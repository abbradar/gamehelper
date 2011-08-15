from django.conf import settings
from importlib import import_module

GAME_CLASSES_CHOICES = {}
for game_class in settings.GAME_CLASSES:
  import_module('game', game_class)
  GAME_CLASSES_CHOICES[game_class] = game.Game.Name
