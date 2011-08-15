from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout, password_change
from registration.views import UserCreateView, UserDetailView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^accounts/login/$',  login, {'next': '/accounts/profile/me'}, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),    
    url(r'^accounts/registration/$', UserCreateView.as_view(success_url='/accounts/login/'), name='user_create'),
    url(r'^accounts/profile/(?P<pk>\d+|me)$', UserDetailView.as_view(), name='user_detail'),
    url(r'^accounts/chpasswd/$', password_change, {'post_change_redirect': '/accounts/profile/me'}, name='password_change'),
    
    url(r'^', include('gamemanager.urls')),
)
