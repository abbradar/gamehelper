from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class UserMessage(models.Model):
  creation_time = models.DateTimeField(auto_now_add=True, editable=False)
  modification_time = models.DateTimeField(auto_now_add=True, editable=False)
  sending_time = models.DateTimeField(editable=False, null=True, blank=True, default=None)
  subject = models.CharField(max_length=100, verbose_name=_('Subject'), blank=True)
  text = models.TextField(verbose_name=_('Text'), blank=True)
  sender = models.ForeignKey(User, related_name='usermessage_sender', verbose_name=_('Sender'), db_index=True)
  sender_copy = models.BooleanField(default=True)
  receivers = models.ManyToManyField(User, blank=True, through='UserMessageCopy')
  refcount = models.IntegerField()
  
  @models.permalink
  def get_absolute_url(self):
    return ('message_detail', (), {'pk': self.id})

  class Meta:
    get_latest_by = "modification_time"
    ordering = ['-modification_time']

class UserMessageCopy(models.Model):
  message = models.ForeignKey(UserMessage)
  user = models.ForeignKey(User, db_index=True)
  copy = models.BooleanField(default=False)
  unread = models.BooleanField(default=True)
