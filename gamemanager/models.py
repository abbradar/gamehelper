from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class Message(models.Model):
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='message_sender')
    receiver = models.ForeignKey(User, related_name='message_receiver')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_ingame = models.BooleanField()
    is_read = models.BooleanField(default=False)
    subject = models.CharField(max_length=100)
    text = models.TextField()

class Game(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=30)
    public_description = models.TextField(verbose_name=_('Public description'))
    protected_description = models.TextField(verbose_name=_('Protected description'))
    #type = models.TextField(verbose_name=_('Type'), max_length=80)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(verbose_name=_('Active'), default=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Game')
        verbose_name_plural = _('Games')

class GameUser(models.Model):
    master = models.ForeignKey(User)
    game = models.ForeignKey(Game, null=True, on_delete=models.SET_NULL)
    notes = models.TextField()
    is_character = models.BooleanField()
    is_gamemaster = models.BooleanField()

class GameMessage(Message):
    game_sender = models.ForeignKey(GameUser, null=True, on_delete=models.SET_NULL, related_name='message_sender')
    game_receiver = models.ForeignKey(GameUser, related_name='message_receiver')

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
