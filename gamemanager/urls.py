from django.conf.urls.defaults import patterns, url
from . import views
from misc.urls import abs_url
from django.views.generic import RedirectView

# todo: replace abs_url with reverse_lazy
urlpatterns = patterns('',
    url(r'^games/list/$', views.GameListView.as_view(), name='game_list'),
    url(r'^games/create/$', views.GameCreateTypeView.as_view(success_url=abs_url("/games/create/%(type)s/")), name='game_create'),
    url(r'^games/create/(?P<type>\w+(?:\.\w+)*)/$', views.GameCreateView.as_view(success_url=abs_url("/games/detail/%(id)i/"))),
    url(r'^games/detail/(?P<game_pk>\d+)/$', views.GameDetailView.as_view(default=True), name='game_detail'),
    url(r'^games/detail/(?P<game_pk>\d+)/(?P<path>.+)$', views.GameDetailView.as_view()),
    url(r'^games/update/(?P<game_pk>\d+)/$', views.GameUpdateView.as_view(success_url=abs_url("/games/detail/%(id)i/")), name='game_update'),
    url(r'^accounts/detail/(?P<pk>\d+|me)/characters/$', views.CharacterListView.as_view(), name='character_list'),
    url(r'^characters/create/$', views.CharacterCreateTypeView.as_view(success_url=abs_url("/characters/create/%(type)s/")), name='character_create'),
    url(r'^characters/create/(?P<type>\w+(?:\.\w+)*)/$', views.CharacterCreateView.as_view(success_url=abs_url("/characters/detail/%(id)i/"))),
    url(r'^characters/detail/(?P<char_pk>\d+)/$', views.CharacterDetailView.as_view(default=True), name='character_detail'),
    url(r'^characters/detail/(?P<char_pk>\d+)/(?P<path>.+)$', views.CharacterDetailView.as_view()),
    url(r'^characters/update/(?P<char_pk>\d+)/$', views.CharacterUpdateView.as_view(success_url=abs_url("/characters/detail/%(id)i/")), name='character_update'),   
)
