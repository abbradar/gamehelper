from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, ListView, DetailView, CreateView
from django.views.generic.edit import ModelFormMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.core import exceptions
from django.http import HttpResponseRedirect, Http404
from django.utils.translation import ugettext as _
from .forms import GameCreateForm
from . import models
from .game_types import GameTypeForm, game_types

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
        game_masters = models.GameMaster.objects.filter(game=self.object.id)
        characters = models.Character.objects.filter(game=self.object.id)
        context['game_masters'] = game_masters
        context['characters'] = characters
        if self.request.user.is_authenticated:
            gm = game_masters.filter(master=self.request.user.id)
            if len(gm) is not 0:
                context['my_gm'] = gm[0]
                context['view_protected'] = True
            if self.request.user.has_perm('gamemanager.view_protected_game'):
                context['view_protected'] = True
        return context

class GameTypeView(FormView):
    form_class = GameTypeForm
    type_field_name = 'type'
    template_name = 'gamemanager/game_create.html'
    
    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url() % {self.type_field_name: form.cleaned_data['type']})
    
    @method_decorator(permission_required('gamemanager.create_game'))
    def dispatch(self, *args, **kwargs):
        return super(GameTypeView, self).dispatch(*args, **kwargs)

class GameCreateView(CreateView):
    game_type_field_name = 'type'
    template_name = 'gamemanager/game_create.html'
    
    def get_form_class(self):
        try:
            game_type = self.kwargs[self.game_type_field_name]
        except KeyError:
            raise exceptions.ImproperlyConfigured('No game type to load form. Please, specify game type.')
        try:
            return game_types.classes[game_type].game_create_form
        except KeyError:
            raise Http404(_(u"No %(game_type)s found matching the query") % {'game_type': game_type})
    
    def form_valid(self, form):
        self.object = form.save()
        gm = models.GameMaster(master = self.request.user, game = self.object)
        gm.save()
        return super(ModelFormMixin, self).form_valid(form)
    
    @method_decorator(permission_required('gamemanager.create_game'))
    def dispatch(self, *args, **kwargs):
        return super(GameCreateView, self).dispatch(*args, **kwargs)
