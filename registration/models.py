from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.db.models.signals import post_save

@models.permalink
def user_get_absolute_url(self):
        return ('user_detail', (), {'pk': self.id})

User.get_absolute_url = user_get_absolute_url

def post_user_create(instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

def default_group_append(instance, created, **kwargs):
    if created and settings.ADD_USERS_TO_DEFAULT_GROUP:
        name = settings.DEFAULT_GROUP_NAME
        group, created = Group.objects.get_or_create(name=name)
        instance.groups.add(group)

post_save.connect(default_group_append, sender=User)
post_save.connect(post_user_create, sender=User)
