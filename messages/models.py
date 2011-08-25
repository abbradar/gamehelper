from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Text(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=100, verbose_name=_('Subject'))
    text = models.TextField(verbose_name=_('Text'))
    
    class Meta:
        get_latest_by = "timestamp"
        ordering = ['-timestamp']
        abstract = True

class UserMessage(Text):
    sender = models.ForeignKey(User, related_name='usermessage_sender', verbose_name=_('Sender'))
    receiver = models.ForeignKey(User, related_name='usermessage_receiver', verbose_name=_('Receiver'))
    sent = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    
    @models.permalink
    def get_absolute_url(self):
        return ('message_detail', (), {'pk': self.id})