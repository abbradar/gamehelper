from django.forms import ModelForm
from .models import Game, Character

class GameCreateForm(ModelForm):
    class Meta:
        model = Game

class GameUpdateForm(ModelForm):
    class Meta:
        model = Game
        fields = ('description', 'active')

class CharacterCreateForm(ModelForm):
    class Meta:
        model = Character
        fields = ('name', 'description')
