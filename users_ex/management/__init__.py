from django.contrib.auth import models
from django.db.models.signals import post_syncdb
from django.conf import settings
from django.db import IntegrityError

def default_group(app, created_models, **kwargs):
  if settings.ADD_USERS_TO_DEFAULT_GROUP:
    if models.Group in created_models:
      name = settings.DEFAULT_GROUP_NAME
      try:
        models.Group.objects.create(name=name)
      except IntegrityError:
        pass

post_syncdb.connect(default_group, sender=models)
