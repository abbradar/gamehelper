from datetime import datetime
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.db.models import Q
from .models import *
from .forms import *

class MessageListView(ListView):
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(MessageListView, self).dispatch(*args, **kwargs)

class MessageReceivedView(MessageListView):
  template_name='messages/message_received.html'
  queryset = UserMessage.objects.exclude(sending_time=None).filter(usermessagecopy__copy=True)
  
  def get_queryset(self):
    return self.queryset.exclude(sender=self.request.user).filter(receivers=self.request.user)

class MessageSentView(MessageListView):
  template_name='messages/message_sent.html'
  queryset = UserMessage.objects.exclude(sending_time=None).filter(sender_copy=True)
  
  def get_queryset(self):
    return self.queryset.filter(sender=self.request.user)

class MessageDraftsView(MessageListView):
  template_name='messages/message_drafts.html'
  queryset = UserMessage.objects.filter(sending_time=None, sender_copy=True)
  
  def get_queryset(self):
    return self.queryset.filter(sender=self.request.user)

class MessageCreateView(CreateView):
  form_class = UserMessageForm
  model = UserMessage
  template_name='messages/message_create.html'

  def get_form_kwargs(self):
    kwargs = CreateView.get_form_kwargs(self)
    kwargs['userid'] = self.request.user.pk
    return kwargs
  
  @method_decorator(permission_required('messages.add_usermessage'))
  def dispatch(self, *args, **kwargs):
    return super(MessageCreateView, self).dispatch(*args, **kwargs)
  
  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.sender = self.request.user
    if form.cleaned_data['send']:
      self.object.refcount = 1 + len(form.cleaned_data['receivers'])
      self.object.sending_time = datetime.now()
    else:
      self.object.refcount = 1
    self.object.save()
    for recipient in form.cleaned_data['receivers']:
      copy = UserMessageCopy(message=self.object, user=recipient, copy=form.cleaned_data['send'])
      copy.save()
    return FormMixin.form_valid(self, form)

class MessageUpdateView(UpdateView):
  form_class = UserMessageForm
  queryset = UserMessage.objects.filter(sending_time=None)
  template_name='messages/message_update.html'

  def get_form_kwargs(self):
    kwargs = UpdateView.get_form_kwargs(self)
    kwargs['userid'] = self.request.user.pk
    return kwargs
  
  @method_decorator(permission_required('messages.add_usermessage'))
  def dispatch(self, *args, **kwargs):
    return super(MessageUpdateView, self).dispatch(*args, **kwargs)
  
  def get_queryset(self):
    return self.queryset.filter(sender=self.request.user)

  def form_valid(self, form):
    self.object = form.save(commit=False)
    if form.cleaned_data['send']:
      self.object.refcount = 1 + len(form.cleaned_data['receivers'])
      self.object.sending_time = datetime.now()
    self.object.save()
    UserMessageCopy.objects.filter(message=self.object).exclude(user__in=form.cleaned_data['receivers']).delete()
    old_receivers = UserMessageCopy.objects.filter(message=self.object)
    old_list = old_receivers.values_list('user', flat=True)
    for recipient in form.cleaned_data['receivers']:
      if not recipient.pk in old_list:
        copy = UserMessageCopy(message=self.object, user=recipient, copy=False)
        copy.save()
    if form.cleaned_data['send']:
      old_receivers.update(copy=True)
    return FormMixin.form_valid(self, form)

class MessageDetailView(DetailView):
  form_class = UserMessageForm
  model = UserMessage
  template_name='messages/message_detail.html'
  
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(MessageDetailView, self).dispatch(*args, **kwargs)
  
  def get_queryset(self):
    return self.model.objects.filter(Q(sender=self.request.user, sender_copy=True) |
        Q(receivers=self.request.user, usermessagecopy__copy=True))

class MessageDeleteView(DeleteView):
  template_name='messages/message_confirm_delete.html'
  model = UserMessage
  
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(MessageDeleteView, self).dispatch(*args, **kwargs)
  
  def get_queryset(self):
    return self.model.objects.filter(Q(sender=self.request.user, sender_copy=True) |
        Q(receivers=self.request.user, usermessagecopy__copy=True))

  def delete(self, request, *args, **kwargs):
    self.object = self.get_object()
    if self.object.sender == request.user:
      self.object.sender_copy = False
    else:
      copy = UserMessageCopy.objects.get(message=self.object, user=self.request.user)
      copy.copy = False
      copy.save()
    self.object.refcount -= 1
    if self.object.refcount == 0:
      self.object.delete()
    else:
      self.object.save()
    return HttpResponseRedirect(self.get_success_url())
