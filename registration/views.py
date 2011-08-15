from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic import DetailView, FormView
from django.contrib.auth.decorators import login_required

class UserCreateView(FormView):
    form_class = UserCreationForm()
    template_name = 'registration/user_create.html'

class UserDetailView(DetailView):
    model = User
    template_name = 'registration/user_detail.html'
    
    def get_object(self):
        if self.kwargs['pk'] == 'me':
            login_required()
            return self.request.user
        return super(UserDetailView, self).get_object()
