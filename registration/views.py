from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User, Group
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core import exceptions
from django.conf import settings
from .forms import UserUpdateForm

class UserListView(ListView):
    model = User
    template_name = 'registration/user_list.html'

class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/user_create.html'
    
    def form_valid(self, form):
        self.object = form.save()
        if settings.ADD_USERS_TO_DEFAULT_GROUP:
            name = settings.DEFAULT_GROUP_NAME
            group = Group.objects.filter(name=name)
            if len(group):
                group = group[0]
            else:
                group = Group(name=name)
                group.save()
            self.object.groups.add(group)
        return FormMixin.form_valid(form)

class UserDetailView(DetailView):
    model = User
    template_name = 'registration/user_detail.html'
    context_object_name = 'current_user'
    
    def get_object(self):
        if self.kwargs['pk'] == 'me':
            if not self.request.user.is_authenticated():
                # TODO: redirect to login page instead
                raise exceptions.PermissionDenied('You need to login to view your own profile page.')
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
        return FormMixin.get_form_kwargs(self)
