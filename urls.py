from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.models import User

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gamehelper.views.home', name='home'),
    # url(r'^gamehelper/', include('gamehelper.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^accounts/login/$',  'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),    
    url(r'^accounts/registration/$', 'registration.views.register'),
    url(r'^accounts/profile/$', 'registration.views.profile'),
    url(r'^accounts/profile/(?P<object_id>\d+)$', 'registration.views.profile'),
    url(r'^accounts/chpasswd/$', 'django.contrib.auth.views.password_change', {'post_change_redirect': '/accounts/profile/'}),
    
    url(r'^', include('gamemanager.urls')),
)
