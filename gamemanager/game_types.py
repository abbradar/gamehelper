from django.conf import settings
from django.core import exceptions
from django.views.generic import CreateView
from django.utils.translation import ugettext as _
from django.utils.functional import LazyObject
from django.forms import Form, ChoiceField
from .utils import get_class
from .forms import GameCreateForm

# very, VERY awful place - lots of circular dependencies right here
# because of them we cannot use 'choices' in Game model
# hopefully it will not cause problems later
class GameType(object):
    game_create_form = GameCreateForm
    name = "generic_game"
    verbose_name = _("Generic game")

class LazyGameTypes(LazyObject):
    def _setup(self):
        self._wrapped = GameTypes()

class GameTypes(object):
    classes = {}
    choices = []
    
    def __init__(self):
        choices_dict = {}
        for game_class in settings.GAME_TYPE_CLASSES:
            gt_class = get_class(game_class)()
            if gt_class.name in self.classes:
               raise exceptions.ImproperlyConfigured('Game type class with name "%(name)" already exists. Change name of "%(class)".' % {'name': gt_class.name, 'class': game_class})
            self.classes[gt_class.name] = gt_class
            if gt_class.verbose_name in choices_dict:
               raise exceptions.ImproperlyConfigured('Game type class with verbose name "%(name)" already exists. Change name of "%(class)".' % {'name': gt_class.verbose_name, 'class': game_class})
            choices_dict[gt_class.name] = gt_class.verbose_name
        self.choices = choices_dict.items()

game_types = LazyGameTypes()

class GameTypeForm(Form):
    type = ChoiceField(choices=game_types.choices)
