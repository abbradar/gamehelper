from django.conf.urls.defaults import patterns, url
from django.contrib.auth.views import login, logout, password_change
from registration.views import UserCreateView, UserDetailView, UserUpdateView, UserPasswordChangeView

urlpatterns = patterns('',
    url(r'^accounts/login/$',  login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),    
    url(r'^accounts/register/$', UserCreateView.as_view(success_url='/accounts/login/'), name='user_create'),
    url(r'^accounts/view/(?P<pk>\d+|me)/$', UserDetailView.as_view(), name='user_detail'),
    url(r'^accounts/passwd/$', UserPasswordChangeView.as_view(success_url='/accounts/view/me/'), name='password_change'),
    url(r'^accounts/change/$', UserUpdateView.as_view(success_url='/accounts/view/me/'), name='user_change'),
)
