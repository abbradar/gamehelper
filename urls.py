from django.conf.urls.defaults import patterns, include, url
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'', include('registration.urls')),
    url(r'', include('gamemanager.urls')),
    url(r'^$', RedirectView.as_view(url="/games/list/")),
)
