from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Text(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100)
    text = models.TextField()
    
    class Meta:
        get_latest_by = "timestamp"
        ordering = ['-timestamp']

class Message(Text):
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='message_sender')
    receiver = models.ForeignKey(User, related_name='message_receiver')

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
        return ('game_news', (), {'game_pk': self.id})
    
    class Meta:
        verbose_name = _('Game')
        verbose_name_plural = _('Games')
        permissions = (
            ('view_protected', 'Can view protected fields'),
        )
        get_latest_by = "creation_date"
        ordering = ['-last_active']

class GameUser(models.Model):
    master = models.ForeignKey(User)
    game = models.ForeignKey(Game, null=True, on_delete=models.SET_NULL)
    
    class Meta:
        permissions = (
            ('view_protected', 'Can view protected fields'),
        )

class Post(Text):
    sender = models.ForeignKey(GameUser, null=True, on_delete=models.SET_NULL, related_name='post_sender')
    game = models.ForeignKey(Game)
    type = models.CharField(max_length=10)

class GameMessage(Text):
    sender = models.ForeignKey(GameUser, null=True, on_delete=models.SET_NULL, related_name='gamemessage_sender')
    receiver = models.ForeignKey(GameUser, related_name='gamemessage_receiver')

class Character(GameUser):
    name = models.CharField(verbose_name=_('Name'), max_length=30)
    description = models.TextField(verbose_name=_('Description'))
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('character_detail', (), {'pk': self.id})
    
    class Meta:
        verbose_name = _('Character')
        verbose_name_plural = _('Characters')

class GameMaster(GameUser):
    pass
