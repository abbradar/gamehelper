from django.forms import ModelForm
from gamemanager.models import Game
class GameCreateForm(ModelForm):
    class Meta:
        model = Game
