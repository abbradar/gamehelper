from django.conf.urls.defaults import patterns, url
from django.contrib.auth.views import login, logout, password_change
from . import views
from misc.urls import abs_url

# todo: replace abs_url with reverse_lazy
urlpatterns = patterns('',
    url(r'^list/$', views.UserListView.as_view(), name='user_list'),
    url(r'^login/$',  login, {'template_name': 'users_ex/login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'users_ex/logged_out.html'}, name='logout'),    
    url(r'^register/$', views.UserCreateView.as_view(success_url=abs_url('/users/login/')), name='user_create'),
    url(r'^detail/(?P<pk>\d+|me)/$', views.UserDetailView.as_view(), name='user_detail'),
    url(r'^passwd/$', views.UserPasswordChangeView.as_view(success_url=abs_url('/users/detail/me/')), name='password_change'),
    url(r'^change/$', views.UserUpdateView.as_view(success_url=abs_url('/users/detail/me/')), name='user_change'),
)
