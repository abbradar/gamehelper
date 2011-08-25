from django.conf.urls.defaults import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin
from misc.urls import abs_regex, abs_url

admin.autodiscover()

urlpatterns = patterns('',
    url(abs_regex(r'^admin/doc/'), include('django.contrib.admindocs.urls')),
    url(abs_regex(r'^admin/'), include(admin.site.urls)),
    
    url(abs_regex(r'^accounts/'), include('users_ex.urls')),
    url(abs_regex(r'^'), include('games.urls')),
    url(abs_regex(r'^$'), RedirectView.as_view(url=abs_url('/games/list/'))),
)
