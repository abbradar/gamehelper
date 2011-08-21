from django.views.generic import ListView, DetailView
from . import models

def get_game_context(request, **kwargs):
    context = {}
    if "game" in kwargs:
        game = kwargs['game']
    else:
        game = models.Game.objects.get(id=kwargs['game_pk'])
    game_masters = models.GameMaster.objects.filter(game=game.id)
    characters = models.Character.objects.filter(game=game.id)
    context['game'] = game
    context['game_masters'] = game_masters
    context['characters'] = characters
    if request.user.is_authenticated:
        gm = game_masters.filter(master=request.user.id, game=game.id)
        if len(gm):
            context['my_gm'] = gm[0]
            context['view_protected'] = True
            context['can_update'] = True
        else:
            if request.user.has_perm('gamemanager.update_game'):
                context['can_update'] = True
    return context

class GameNewsListView(ListView):
    template_name = "gamemanager/game_news.html"
    
    def get_queryset(self):
        return models.Post.objects.filter(type='news', game_id=self.kwargs['game_pk'])
    
    def get_context_data(self, **kwargs):
        context = super(GameNewsListView, self).get_context_data(**kwargs)
        context.update(get_game_context(self.request, **self.kwargs))
        return context

def get_character_context(request, **kwargs):
    context = {}
    if "character" in kwargs:
        character = kwargs['character']
    else:
        character = models.Character.objects.get(id=kwargs['char_pk'])
    context['character'] = character
    if request.user.is_authenticated:
        if character.master_id == request.user.id:
            context['can_update'] = True                 
    return context

class CharacterOverviewView(DetailView):
    model = models.Character
    template_name = "gamemanager/character_detail.html"
    pk_url_kwarg = 'char_pk'
    
    def get_context_data(self, **kwargs):
        context = super(CharacterOverviewView, self).get_context_data(**kwargs)
        context.update(get_character_context(self.request, **self.kwargs))
        return context
