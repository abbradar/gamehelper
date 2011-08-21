from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Text(models.Model):
    creator = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100)
    text = models.TextField()
    
    class Meta:
        get_latest_by = "timestamp"
        ordering = ['-timestamp']

class Message(Text):
    receiver = models.ForeignKey(User)

class Game(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=30)
    description = models.TextField(blank=True, verbose_name=_('Description'))
    type = models.TextField(verbose_name=_('Type'), max_length=30, editable=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(verbose_name=_('Active'), default=True)
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('game_detail', (), {'game_pk': self.id})
    
    def get_type_class(self):
        from .game_types import game_types
        return game_types.classes[self.type]
    
    class Meta:
        verbose_name = _('Game')
        verbose_name_plural = _('Games')
        get_latest_by = "creation_date"
        ordering = ['-last_active']

class GameUser(models.Model):
    master = models.ForeignKey(User)
    type = models.TextField(verbose_name=_('Type'), max_length=30, editable=False)

class Post(Text):
    game = models.ForeignKey(Game)
    type = models.CharField(max_length=10)

class GameMessage(Text):
    receiver = models.ForeignKey(GameUser)

class Character(GameUser):
    name = models.CharField(verbose_name=_('Name'), max_length=30)
    description = models.TextField(verbose_name=_('Description'))
    game = models.ForeignKey(Game, null=True, on_delete=models.SET_NULL)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('character_detail', (), {'char_pk': self.id})
    
    def get_type_class(self):
        from .game_types import game_types
        return game_types.classes[self.type]
    
    class Meta:
        verbose_name = _('Character')
        verbose_name_plural = _('Characters')

class GameMaster(GameUser):
    game = models.ForeignKey(Game)
