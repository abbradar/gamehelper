from django.forms import ModelForm
from games.models import Game, Character

class GameUpdateForm(ModelForm):
    class Meta:
        model = Game
        fields = ('description', 'active')

class CharacterCreateForm(ModelForm):
    class Meta:
        model = Character
        fields = ('name', 'description')
