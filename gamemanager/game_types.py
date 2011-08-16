from django.conf import settings
from django.utils.importlib import import_module
from django.core import exceptions

def get_game_type_choices():
    gt_list = {}
    for game_class in settings.GAME_TYPE_CLASSES:
        try:
            gt_module, gt_classname = game_class.rsplit('.', 1)
        except ValueError:
            raise exceptions.ImproperlyConfigured('%s isn\'t a game type class' % game_class)
        try:
            mod = import_module(gt_module)
        except ImportError, e:
            raise exceptions.ImproperlyConfigured('Error importing game type %s: "%s"' % (gt_module, e))
        try:
            gt_class = getattr(mod, gt_classname)
        except AttributeError:
            raise exceptions.ImproperlyConfigured('Game type module "%s" does not define a "%s" class' % (gt_module, gt_classname))
        verbose_name = getattr(gt_class, 'verbose_name', game_class)
        if not isinstance(verbose_name, basestring):
           raise exceptions.ImproperlyConfigured('%s isn\'t a valid game type class' % game_class)
        gt_list[verbose_name] = game_class
    return tuple(gt_list.values())

class CreateGameView:
    pass

class GameType:
    create_game_view = None
