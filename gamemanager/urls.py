from django.conf.urls.defaults import patterns, url
from . import views
from utils import abs_url, abs_regex
from django.views.generic import RedirectView

# todo: replace abs_url with reverse_lazy
urlpatterns = patterns('',
    url(r'^list/$', views.GameListView.as_view(), name='game_list'),
    url(r'^detail/(?P<game_pk>\d+)/$', views.game_detail_view, name='game_detail'),
    url(r'^detail/(?P<game_pk>\d+)/(?P<regex>.+)$', views.game_resolve_view),
    url(r'^update/(?P<game_pk>\d+)/$', views.GameUpdateView.as_view(success_url=abs_url("/games/detail/%(id)i/")), name='game_update'),
    url(r'^create/$', views.GameTypeView.as_view(success_url=abs_url("/games/create/%(type)s/")), name='game_create'),
    url(r'^create/(?P<type>\w+(?:\.\w+)*)/$', views.GameCreateView.as_view(success_url=abs_url("/games/detail/%(id)i/"))),
)
