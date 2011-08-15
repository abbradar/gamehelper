from gamemanager import models
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

class GameListView(ListView):
    template_name = "gamemanager/game_list.html"
    model = models.Game

    def get_context_data(self, **kwargs):
        context = super(GameListView, self).get_context_data(**kwargs)
        if self.request.user.has_perm('gamemanager.create_game'):
            context['can_create'] = True
        return context

class GameDetailView(DetailView):
    template_name = "gamemanager/game_detail.html"
    model = models.Game
  
    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
          gm = models.GameMaster.objects.filter(master=self.request.user.id, game=self.object.id)
          if len(gm) is not 0:
            context['game_master'] = gm[0]
        if 'game_master' in context or self.request.user.has_perm('gamemanager.view_protected_game'):
            context['view_protected'] = True
        return context

class GameCreateView(CreateView):
    model = models.Game
    
    @method_decorator(permission_required('gamemanager.create_game'))
    def dispatch(self, *args, **kwargs):
        return super(GameCreateView, self).dispatch(*args, **kwargs)
