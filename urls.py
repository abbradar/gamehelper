from django.conf.urls.defaults import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy

admin.autodiscover()

urlpatterns = patterns('',
  url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
  url(r'^admin/', include(admin.site.urls)),
  
  url(r'^users/', include('users_ex.urls')),
  url(r'^messages/', include('messages.urls')),
  url(r'^', include('games.urls')),
  url(r'^$', RedirectView.as_view(url=reverse_lazy('game_list'))),
)
