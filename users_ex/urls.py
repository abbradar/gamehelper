from django.conf.urls.defaults import patterns, url
from django.contrib.auth.views import login, logout, password_change
from django.core.urlresolvers import reverse_lazy
from . import views

urlpatterns = patterns('',
    url(r'^list/$', views.UserListView.as_view(), name='user_list'),
    url(r'^login/$',  login, {'template_name': 'users_ex/login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'users_ex/logged_out.html'}, name='logout'),
    url(r'^register/$', views.UserCreateView.as_view(success_url=reverse_lazy('login')), name='user_create'),
    url(r'^detail/(?P<pk>\d+|me)/$', views.UserDetailView.as_view(), name='user_detail'),
    url(r'^passwd/$', views.UserPasswordChangeView.as_view(), name='password_change'),
    url(r'^change/$', views.UserUpdateView.as_view(), name='user_change'),
)
