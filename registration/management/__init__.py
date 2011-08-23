from django.contrib.auth import models
from django.db.models.signals import post_syncdb
from django.conf import settings

def default_group(app, created_models, **kwargs):
    if models.Group in created_models:
        if settings.ADD_USERS_TO_DEFAULT_GROUP:
            group = models.Group(name=name)
            group.save()

post_syncdb.connect(default_group, sender=models)
