from django.conf import settings
from django.core import exceptions
from django.views.generic import CreateView
from django.utils.functional import LazyObject
from django.forms import Form, ChoiceField
from misc.utils import get_class

class GameType(object):
    def __unicode__(self):
        return getattr(self, 'verbose_name', self.name)

class LazyGameTypes(LazyObject):
    def _setup(self):
        self._wrapped = GameTypes()

class GameTypes(object): 
    def __init__(self):
        self._classes = {}
        self._names = {}
        for game_class in settings.GAME_TYPE_CLASSES:
            gt_class = get_class(game_class)
            gt_class = gt_class()
            if gt_class.name in self._classes:
               raise exceptions.ImproperlyConfigured('Game type class with name "%(name)" already exists. Change name of "%(class)".' % {'name': gt_class.name, 'class': game_class})
            self._classes[gt_class.name] = gt_class
            verbose_name = unicode(gt_class)
            if verbose_name in self._names.values():
               raise exceptions.ImproperlyConfigured('Game type class with verbose name "%(name)" already exists. Change name of "%(class)".' % {'name': gt_class.verbose_name, 'class': game_class})
            self._names[gt_class.name] = verbose_name
    
    @property
    def classes(self):
        return self._classes
    
    @property
    def names(self):
        return self._names

game_types = LazyGameTypes()

class GameTypeForm(Form):
    type = ChoiceField(choices=game_types.names.items())
