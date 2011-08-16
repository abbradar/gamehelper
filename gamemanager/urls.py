from django.conf.urls.defaults import patterns, url
from gamemanager import views
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^games/list/$', views.GameListView.as_view(), name='game_list'),
    url(r'^games/detail/(?P<pk>\d+)/$', views.GameDetailView.as_view(), name='game_detail'),
    url(r'^games/create/$', views.GameCreateView.as_view(success_url="/games/detail/%(id)"), name='game_create'),
)
