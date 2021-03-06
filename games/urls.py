from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse_lazy
from . import views
from django.views.generic import RedirectView

urlpatterns = patterns('',
  url(r'^games/list/$', views.GameListView.as_view(), name='game_list'),
  url(r'^games/create/$', views.GameCreateTypeView.as_view(get_typed_url=lambda (type): 
    reverse_lazy('game_create_typed', kwargs={'type': type})), name='game_create'),
  url(r'^games/create/(?P<type>\w+(?:\.\w+)*)/$', views.GameCreateView.as_view(), name='game_create_typed'),
  url(r'^games/detail/(?P<game_pk>\d+)/(?P<path>.*)$', views.game_detail_view.dispatch, name='game_detail'),
  url(r'^games/update/(?P<game_pk>\d+)/$', views.GameUpdateView.as_view(), name='game_update'),
  url(r'^games/delete/(?P<game_pk>\d+)/$', views.GameDeleteView.as_view(), {'success_url': reverse_lazy('game_list')}, name='game_delete'),
  url(r'^users/detail/(?P<pk>\d+|me)/characters/$', views.CharacterListView.as_view(), name='character_list'),
  url(r'^characters/create/$', views.CharacterCreateTypeView.as_view(get_typed_url=lambda (type): 
    reverse_lazy('character_create_typed', kwargs={'type': type})), name='character_create'),
  url(r'^characters/create/(?P<type>\w+(?:\.\w+)*)/$', views.CharacterCreateView.as_view(), name='character_create_typed'),
  url(r'^characters/detail/(?P<char_pk>\d+)/(?P<path>.*)$', views.character_detail_view.dispatch, name='character_detail'),
  url(r'^characters/update/(?P<char_pk>\d+)/$', views.CharacterUpdateView.as_view(), name='character_update'),
  url(r'^characters/delete/(?P<char_pk>\d+)/$', views.CharacterDeleteView.as_view(get_usered_url=
    lambda(user): reverse_lazy('character_list', kwargs={'pk': user})), name='character_delete'),
)
