from django.forms import ModelForm
from .models import Game

class GameCreateForm(ModelForm):
    class Meta:
        model = Game
