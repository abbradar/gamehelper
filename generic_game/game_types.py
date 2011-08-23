from .views import *
from django.utils.translation import ugettext as _
import urls

class GameType(object):
    game_create_view = staticmethod(GameCreateView.as_view())
    game_update_view = staticmethod(GameUpdateView.as_view())
    character_create_view = staticmethod(CharacterCreateView.as_view())
    character_update_view = staticmethod(CharacterUpdateView.as_view())
    game_urls = urls.game_urlpatterns
    character_urls = urls.character_urlpatterns
    name = "generic_game"
    verbose_name = _("Generic game")
