from django.conf.urls.defaults import patterns, url
from django.contrib.auth.views import login, logout, password_change
from . import views

urlpatterns = patterns('',
    url(r'^list/$', views.UserListView.as_view(), name='user_list'),
    url(r'^login/$',  login, name='login'),
    url(r'^logout/$', logout, name='logout'),    
    url(r'^register/$', views.UserCreateView.as_view(success_url='/accounts/login/'), name='user_create'),
    url(r'^detail/(?P<pk>\d+|me)/$', views.UserDetailView.as_view(), name='user_detail'),
    url(r'^passwd/$', views.UserPasswordChangeView.as_view(success_url='/accounts/detail/me/'), name='password_change'),
    url(r'^change/$', views.UserUpdateView.as_view(success_url='/accounts/detail/me/'), name='user_change'),
)
