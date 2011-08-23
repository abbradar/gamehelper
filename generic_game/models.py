from django.db import models
from gamemanager.models import *
from django.utils.translation import ugettext as _

class PostCategory(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=30)
    game = models.ForeignKey(Game)
    protected = models.BooleanField()

class Post(Text):
    category = models.ForeignKey(PostCategory)

class GameMessage(Text):
    sender = models.ForeignKey(GameUser, related_name='message_sender')
    receiver = models.ForeignKey(GameUser, related_name='message_receiver')
