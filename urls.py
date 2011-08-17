from django.conf.urls.defaults import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin
from utils import abs_regex, abs_url

admin.autodiscover()

urlpatterns = patterns('',
    url(abs_regex(r'^admin/doc/'), include('django.contrib.admindocs.urls')),
    url(abs_regex(r'^admin/'), include(admin.site.urls)),
    
    url(abs_regex(r'^accounts/'), include('registration.urls')),
    url(abs_regex(r'^games/'), include('gamemanager.urls')),
    url(abs_regex(r'^$'), RedirectView.as_view(url=abs_url("/games/list/"))),
)
