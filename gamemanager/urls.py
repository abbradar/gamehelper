from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import redirect_to
from django.views.generic.list_detail import object_list, object_detail
from gamemanager import models

urlpatterns = patterns('',
    url(r'^$', redirect_to, {'url': 'games/list/'}),
    url(r'^games/list/$', object_list, {'queryset': models.Game.objects.all()}, name='game_list'),
    url(r'^games/list/(?P<page>(?:\d+|last))$', object_list, {'queryset': models.Game.objects.all()}, name='game_list'),
    url(r'^games/(?P<object_id>\d+)$', object_detail, {'queryset': models.Game.objects.all()}, name='game_detail'),
    url(r'^character/(?P<object_id>\d+)$', object_detail, {'queryset': models.Character.objects.all()}, name='character_detail'),
)