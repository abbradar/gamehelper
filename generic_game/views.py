from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.core import exceptions
from django.utils.translation import ugettext as _
from .models import *
from .forms import *
from games.models import *

def get_game_context(request, **kwargs):
    context = {}
    if "game" in kwargs:
        game = kwargs['game']
    else:
        game = Game.objects.get(id=kwargs['game_pk'])
    game_masters = GameMaster.objects.filter(game=game)
    characters = Character.objects.filter(game=game)
    context['game'] = game
    context['game_masters'] = game_masters
    context['characters'] = characters
    if request.user.is_authenticated:
        try:
            if "gm" in kwargs:
                gm = kwargs['gm']
            else:
                gm = game_masters.get(master=request.user, game=game)
            context['gm'] = gm
            context['view_protected'] = True
            context['can_update'] = True
            context['can_delete'] = True
        except exceptions.ObjectDoesNotExist:
            if request.user.has_perm('games.change_game'):
                context['can_update'] = True
            if request.user.has_perm('games.delete_game'):
                context['can_delete'] = True
    return context

class GameCreateView(CreateView):
    model = Game
    template_name = "generic_game/game_create.html"
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.type = self.kwargs['type']
        self.object.save()
        gm = GameMaster(master=self.request.user, game=self.object)
        gm.save()
        return FormMixin.form_valid(self, form)

class GameUpdateView(UpdateView):
    form_class = GameUpdateForm
    template_name = "generic_game/game_update.html"
    
    def get_object(self, queryset=None):
        object = self.kwargs['game']
        self.extra_context = get_game_context(self.request, **self.kwargs)
        return object
    
    def get_context_data(self, **kwargs):
        context = super(GameUpdateView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


class GameDeleteView(DeleteView):
    template_name = "generic_game/game_confirm_delete.html"
    
    def get_object(self, queryset=None):
        return self.kwargs['game']
    
    def get_context_data(self, **kwargs):
        context = super(GameDeleteView, self).get_context_data(**kwargs)
        context.update(get_game_context(self.request, **self.kwargs))
        return context
    
    def get_success_url(self):
        return self.kwargs['success_url']

class GameDetailView(DetailView):
    template_name = "generic_game/game_detail.html"
    
    def get_object(self, queryset=None):
        return self.kwargs['game']
    
    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        context.update(get_game_context(self.request, **self.kwargs))
        return context

def get_character_context(request, **kwargs):
    context = {}
    if "character" in kwargs:
        character = kwargs['character']
    else:
        character = Character.objects.get(id=kwargs['char_pk'])
    context['character'] = character
    if request.user.is_authenticated:
        if character.master == request.user:
            context['can_update'] = True
            context['can_delete'] = True
        else:
            if request.user.has_perm('games.change_character'):
                context['can_update'] = True
            if request.user.has_perm('games.delete_character'):
                context['can_delete'] = True
    return context

class CharacterCreateView(CreateView):
    form_class = CharacterCreateForm
    template_name = "generic_game/character_create.html"
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.type = self.kwargs['type']
        self.object.master = self.request.user
        self.object.save()
        return FormMixin.form_valid(self, form)

class CharacterUpdateView(UpdateView):
    form_class = CharacterCreateForm
    template_name = "generic_game/character_update.html"
    
    def get_object(self, queryset=None):
        return self.kwargs['character']
    
    def get_context_data(self, **kwargs):
        context = super(CharacterUpdateView, self).get_context_data(**kwargs)
        context.update(get_character_context(self.request, **self.kwargs))
        return context

class CharacterDeleteView(DeleteView):
    template_name = "generic_game/character_confirm_delete.html"
    
    def get_object(self, queryset=None):
        return self.kwargs['character']
    
    def get_context_data(self, **kwargs):
        context = super(CharacterDeleteView, self).get_context_data(**kwargs)
        context.update(get_character_context(self.request, **self.kwargs))
        return context
    
    def get_success_url(self):
        return self.kwargs['success_url']

class CharacterDetailView(DetailView):
    template_name = "generic_game/character_detail.html"
    
    def get_object(self, queryset=None):
        return self.kwargs['character']
    
    def get_context_data(self, **kwargs):
        context = super(CharacterDetailView, self).get_context_data(**kwargs)
        context.update(get_character_context(self.request, **self.kwargs))
        return context
