from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    @models.permalink
    def get_absolute_url(self):
        return ('user_detail', (), {'pk': self.id})

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        if settings.ADD_USERS_TO_DEFAULT_GROUP:
            name = settings.DEFAULT_GROUP_NAME
            group = Group.objects.get(name=name)
            instance.groups.add(group)

post_save.connect(create_user_profile, sender=User)
