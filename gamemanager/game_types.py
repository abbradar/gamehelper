from django.conf import settings
from django.core import exceptions
from django.views.generic import CreateView
from django.utils.translation import ugettext as _
from django.utils.functional import LazyObject
from django.forms import Form, ChoiceField
from misc.utils import get_class
from .game_forms import *
from .game_views import *
from . import game_urls as urls

# Very, VERY awful place - lots of circular dependencies lurking in the shadows.
# Because of them we cannot use 'choices' in Game model.
# Hopefully it will not cause problems later.
class GameType(object):
    game_create_form = GameCreateForm
    game_update_form = GameUpdateForm
    character_create_form = CharacterCreateForm
    character_update_form = CharacterCreateForm
    game_urls = (urls.game_urlpatterns, GameNewsListView.as_view())
    character_urls = (urls.character_urlpatterns, CharacterOverviewView.as_view())
    name = "generic_game"
    verbose_name = _("Generic game")

class LazyGameTypes(LazyObject):
    def _setup(self):
        self._wrapped = GameTypes()

class GameTypes(object):
    _classes = {}
    _names = {}
    
    def __init__(self):
        for game_class in settings.GAME_TYPE_CLASSES:
            gt_class = get_class(game_class)
            gt_class = gt_class()
            if gt_class.name in self._classes:
               raise exceptions.ImproperlyConfigured('Game type class with name "%(name)" already exists. Change name of "%(class)".' % {'name': gt_class.name, 'class': game_class})
            self._classes[gt_class.name] = gt_class
            if gt_class.verbose_name in self._names.values():
               raise exceptions.ImproperlyConfigured('Game type class with verbose name "%(name)" already exists. Change name of "%(class)".' % {'name': gt_class.verbose_name, 'class': game_class})
            self._names[gt_class.name] = gt_class.verbose_name
    
    @property
    def classes(self):
        return self._classes
    
    @property
    def names(self):
        return self._names

game_types = LazyGameTypes()

class GameTypeForm(Form):
    type = ChoiceField(choices=game_types.names.items())
