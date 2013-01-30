from django.db import models
from games.models import *
from django.utils.translation import ugettext_lazy as _

class GenericGameMaster(models.Model):
  gameuser = models.OneToOneField(GameUser, primary_key=True, verbose_name=_('Game user'))
  notes = models.TextField(verbose_name=_('Note'))

class WikiPage(RestrictedData):
  game = models.ForeignKey(Game)
  name = models.CharField(max_length=100, verbose_name=_('Name'))
  creation_time = models.DateTimeField(auto_now_add=True, editable=False)
  modification_time = models.DateTimeField(auto_now=True, editable=False)
  text = models.TextField(verbose_name=_('Text'))

class Scene(models.Model):
  game = models.ForeignKey(Game)
  name = models.CharField(max_length=100, verbose_name=_('Name'))
  creation_time = models.DateTimeField(auto_now_add=True, editable=False)
  modification_time = models.DateTimeField(auto_now=True, editable=False)
  summary = models.TextField(verbose_name=_('Summary'))
  gm_notes = models.TextField(verbose_name=_('GM Notes'))

class Thread(RestrictedData):
  game = models.ForeignKey(Game, editable=False)
  creation_time = models.DateTimeField(auto_now_add=True, editable=False)
  modification_time = models.DateTimeField(auto_now=True, editable=False)
  name = models.CharField(max_length=100, verbose_name=_('Name'))
  description = models.CharField(max_length=300, verbose_name=_('Description'))
  creator = models.ForeignKey(User, editable=False)

class ThreadMessage(models.Model):
  thread = models.ForeignKey(Thread, editable=False)
  creation_time = models.DateTimeField(auto_now_add=True, editable=False)
  modification_time = models.DateTimeField(auto_now=True, editable=False)
  creator = models.ForeignKey(User, editable=False)
  subject = models.CharField(max_length=100, verbose_name=_('Subject'))
  text = models.TextField(verbose_name=_('Text'))

class Event(models.Model):
  scene = models.ForeignKey(Scene, editable=False)
  gameuser = models.ForeignKey(GameUser, editable=False)
  creation_time = models.DateTimeField(auto_now_add=True, editable=False)
  modification_time = models.DateTimeField(auto_now=True, editable=False)
  parent = models.ForeignKey('Event', null=True, blank=True, default=None)
  threads = models.ManyToManyField(Thread, null=True, blank=True, default=None)
  text = models.TextField()

  class Meta:
    get_latest_by = "creation_time"
    ordering = ['-creation_time']
