from django import forms
from django.contrib.auth.models import User
from games.models import Game, Character
from django.utils.translation import ugettext_lazy as _

class GameUpdateForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('description', 'active')

class CharacterCreateForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ('name', 'description')

class SelectUserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label=_('User'))
