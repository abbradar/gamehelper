from django.views.generic import ListView
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
        gm = game_masters.filter(master=request.user.id)
        if len(gm):
            context['my_gm'] = gm[0]
            context['view_protected'] = True
            context['can_update'] = True
        else:
            if request.user.has_perm('gamemanager.view_protected_game'):
                context['view_protected'] = True
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
