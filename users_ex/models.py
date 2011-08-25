from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.db.models.signals import post_save

class Text(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100)
    text = models.TextField()
    
    class Meta:
        get_latest_by = "timestamp"
        ordering = ['-timestamp']
        abstract = True

class UserMessage(Text):
    sender = models.ForeignKey(User, related_name='usermessage_sender')
    receiver = models.ForeignKey(User, related_name='usermessage_receiver')
    sent = models.BooleanField()
    received = models.BooleanField()

@models.permalink
def user_get_absolute_url(self):
        return ('user_detail', (), {'pk': self.id})

User.get_absolute_url = user_get_absolute_url

def default_group_append(instance, created, **kwargs):
    if created and settings.ADD_USERS_TO_DEFAULT_GROUP:
        name = settings.DEFAULT_GROUP_NAME
        group, created = Group.objects.get_or_create(name=name)
        instance.groups.add(group)

post_save.connect(default_group_append, sender=User)
