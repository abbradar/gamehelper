from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from .models import *
from .forms import *

class MessageListView(ListView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MessageListView, self).dispatch(*args, **kwargs)

class MessageReceivedView(MessageListView):
    template_name='messages/message_received.html'
    queryset = UserMessage.objects.filter(sent=True)
    
    def get_queryset(self):
        return self.queryset.filter(receiver=self.request.user)

class MessageSentView(MessageListView):
    template_name='messages/message_sent.html'
    queryset = UserMessage.objects.filter(sent=True)
    
    def get_queryset(self):
        return self.queryset.filter(sender=self.request.user)

class MessageDraftsView(MessageListView):
    template_name='messages/message_drafts.html'
    queryset = UserMessage.objects.filter(sent=False)
    
    def get_queryset(self):
        return self.queryset.filter(sender=self.request.user)

class MessageCreateView(CreateView):
    form_class = MessageCreateForm
    model = UserMessage
    template_name='messages/message_create.html'
    
    @method_decorator(permission_required('messages.add_message'))
    def dispatch(self, *args, **kwargs):
        return super(MessageCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.sender = self.request.user
        self.object.save()
        return FormMixin.form_valid(self, form)

class MessageUpdateView(UpdateView):
    form_class = MessageCreateForm
    queryset = UserMessage.objects.filter(sent=False)
    template_name='messages/message_update.html'
    
    @method_decorator(permission_required('messages.add_message'))
    def dispatch(self, *args, **kwargs):
        return super(MessageUpdateView, self).dispatch(*args, **kwargs)
    
    def get_queryset(self):
        return self.queryset.filter(sender=self.request.user)

class MessageDetailView(DetailView):
    form_class = MessageCreateForm
    model = UserMessage
    template_name='messages/message_detail.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MessageDetailView, self).dispatch(*args, **kwargs)
    
    def get_queryset(self):
        return self.model.objects.filter(Q(sender=self.request.user, sent=False)|Q(receiver=self.request.user, sent=True))
