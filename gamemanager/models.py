from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from gamemanager.game_types import get_game_type_choices

class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100)
    text = models.TextField()

class PrivateMessage(Message):
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='private_sender')
    receiver = models.ForeignKey(User, related_name='private_receiver')

class Game(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=30)
    public_description = models.TextField(verbose_name=_('Public description'))
    protected_description = models.TextField(verbose_name=_('Protected description'))
    type = models.TextField(verbose_name=_('Type'), max_length=80, choices=get_game_type_choices())
    creation_date = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(verbose_name=_('Active'), default=True)
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('game_detail', (), {'pk': self.id})
    
    class Meta:
        verbose_name = _('Game')
        verbose_name_plural = _('Games')
        permissions = (
            ('view_protected', 'Can view protected fields'),
        )

class GameUser(models.Model):
    master = models.ForeignKey(User)
    game = models.ForeignKey(Game, null=True, on_delete=models.SET_NULL)
    notes = models.TextField()
    
    class Meta:
        permissions = (
            ('view_protected', 'Can view protected fields'),
        )

class PublicGameMessage(Message):
    sender = models.ForeignKey(GameUser, null=True, on_delete=models.SET_NULL, related_name='publicgame_sender')
    game = models.ForeignKey(Game)

class PrivateGameMessage(Message):
    sender = models.ForeignKey(GameUser, null=True, on_delete=models.SET_NULL, related_name='privategame_sender')
    receiver = models.ForeignKey(GameUser, related_name='privategame_receiver')

class Character(GameUser):
    name = models.CharField(verbose_name=_('Name'), max_length=30)
    public_description = models.TextField(verbose_name=_('Public description'))
    protected_description = models.TextField(verbose_name=_('Protected description'))
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Character')
        verbose_name_plural = _('Characters')

class GameMaster(GameUser):
    name = models.CharField(max_length=30)
