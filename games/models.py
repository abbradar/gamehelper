from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Type(models.Model):
  type = models.CharField(verbose_name=_('Type'), max_length=30, editable=False)
  
  class Meta:
    abstract = True
  
  def get_type_class(self):
    from .game_types import game_types
    return game_types.classes[self.type]

class Game(Type):
  name = models.CharField(verbose_name=_('Name'), max_length=30)
  description = models.TextField(blank=True, verbose_name=_('Description'))
  creation_time = models.DateTimeField(auto_now_add=True, editable=False)
  modification_time = models.DateTimeField(auto_now=True, editable=False)
  active = models.BooleanField(verbose_name=_('Active'), default=True)
  
  def __unicode__(self):
    return self.name
  
  @models.permalink
  def get_absolute_url(self):
    return ('game_detail', (), {'game_pk': self.id, 'path': ''})
  
  class Meta:
    verbose_name = _('Game')
    verbose_name_plural = _('Games')
    get_latest_by = "modification_time"
    ordering = ['-modification_time']

class Character(Type):
  name = models.CharField(verbose_name=_('Name'), max_length=30)
  user = models.ForeignKey(User, db_index=True)
  description = models.TextField(blank=True, verbose_name=_('Description'))
  creation_time = models.DateTimeField(auto_now_add=True, editable=False)
  modification_time = models.DateTimeField(auto_now=True, editable=False)
  
  def __unicode__(self):
    return self.name
  
  @models.permalink
  def get_absolute_url(self):
    return ('character_detail', (), {'char_pk': self.id, 'path': ''})
  
  class Meta:
    verbose_name = _('Character')
    verbose_name_plural = _('Characters')

class RestrictedData(models.Model):
  ALL = 'A'
  GAMEMASTER = 'G'
  PERMISSION_CHOICES = (
      (ALL, _('All')),
      (GAMEMASTER, _('Gamemaster')),
  )

  permissions = models.CharField(verbose_name=_('Permissions'), max_length=1, choices=PERMISSION_CHOICES)

  class Meta:
    abstract = True

class GameUser(Type):
  game = models.ForeignKey(Game, db_index=True, editable=False)
  character = models.ForeignKey(Character, null=True, blank=True, verbose_name=_('Character'), editable=False)
  gamemaster = models.ForeignKey(User, null=True, blank=True, verbose_name=_('Gamemaster'), editable=False)
