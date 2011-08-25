from django.db import models
from games.models import *
from messages.models import Text
from django.utils.translation import ugettext_lazy as _

class PostCategory(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=30)
    game = models.ForeignKey(Game)
    protected = models.BooleanField()

class GameMessage(Text):
    sender = models.ForeignKey(GameUser, related_name='message_sender')
    receiver = models.ForeignKey(GameUser, related_name='message_receiver')
