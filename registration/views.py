from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserUpdateForm

class UserListView(ListView):
    model = User
    template_name = 'registration/user_list.html'

class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/user_create.html'

class UserDetailView(DetailView):
    model = User
    template_name = 'registration/user_detail.html'
    context_object_name = 'current_user'
    
    def get_object(self):
        if self.kwargs['pk'] == 'me':
            login_required()
            return self.request.user
        return super(UserDetailView, self).get_object()

class UserPrivateView(UpdateView):
    model = User
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserPrivateView, self).dispatch(*args, **kwargs)
    
    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserPrivateView, self).get_context_data(**kwargs)
        context['current_user'] = self.get_object()
        return context

class UserUpdateView(UserPrivateView):
    form_class = UserUpdateForm
    template_name = 'registration/user_update.html'

class UserPasswordChangeView(UserPrivateView):
    form_class = PasswordChangeForm
    template_name = 'registration/user_password_change.html'
    
    # not so beautiful as it should be - blame PasswordChangeForm being not ModelForm
    # (we should not send 'instance' to form, and instead send object there)
    def get_form(self, form_class):
        return form_class(self.get_object(), **self.get_form_kwargs())
    
    def get_form_kwargs(self):
        return super(ModelFormMixin, self).get_form_kwargs()
