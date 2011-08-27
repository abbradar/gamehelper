from django.conf.urls.defaults import patterns, url
from views import *

game_urlpatterns = patterns('',
    url('^$', GameDetailView.as_view(), name='game_detail'),
)

character_urlpatterns = patterns('',
    url('^$', CharacterDetailView.as_view(), name='character_detail'),
)
