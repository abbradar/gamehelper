from django.conf.urls.defaults import patterns, url
from . import views
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^list/$', views.GameListView.as_view(), name='game_list'),
    url(r'^detail/(?P<pk>\d+)/$', views.GameDetailView.as_view(), name='game_detail'),
    url(r'^create/$', views.GameTypeView.as_view(success_url="/games/create/%(type)s/"), name='game_create'),
    url(r'^create/(?P<type>\w+(?:\.\w+)*)/$', views.GameCreateView.as_view(success_url="/games/detail/%(id)i/")),
)
