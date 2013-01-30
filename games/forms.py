from django import forms
from django.contrib.auth.models import User
from .models import Game, Character
from django.utils.translation import ugettext_lazy as _

class GameUpdateForm(forms.ModelForm):
  class Meta:
    model = Game
    fields = ('active', 'description')

class CharacterCreateForm(forms.ModelForm):
  class Meta:
    model = Character
    fields = ('name', 'description')
