from django.conf.urls.defaults import patterns, url
from . import views
from utils import abs_url, abs_regex
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^list/$', views.GameListView.as_view(), name='game_list'),
    url(r'^news/(?P<game_pk>\d+)/$', views.GameNewsListView.as_view(), name='game_news'),
    url(r'^update/(?P<game_pk>\d+)/$', views.GameUpdateView.as_view(success_url=abs_url("/games/news/%(id)i/")), name='game_update'),
    url(r'^create/$', views.GameTypeView.as_view(success_url=abs_url("/games/create/%(type)s/")), name='game_create'),
    url(r'^create/(?P<type>\w+(?:\.\w+)*)/$', views.GameCreateView.as_view(success_url=abs_url("/games/news/%(id)i/"))),
)
