from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import FormMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.core import exceptions
from .models import *
from .forms import *
from gamemanager.models import *

def get_game_context(request, **kwargs):
    context = {}
    if "game" in kwargs:
        game = kwargs['game']
    else:
        game = Game.objects.get(id=kwargs['game_pk'])
    game_masters = GameMaster.objects.filter(game=game.id)
    characters = Character.objects.filter(game=game.id)
    context['game'] = game
    context['game_masters'] = game_masters
    context['characters'] = characters
    if request.user.is_authenticated:
        try:
            gm = game_masters.get(master=request.user.id, game=game.id)
            context['my_gm'] = gm
            context['view_protected'] = True
            context['can_update'] = True
        except exceptions.ObjectDoesNotExist:
            if request.user.has_perm('gamemanager.change_game'):
                context['can_update'] = True
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
    
    @method_decorator(permission_required('gamemanager.add_game'))
    def dispatch(self, *args, **kwargs):
        return super(GameCreateView, self).dispatch(*args, **kwargs)

class GameUpdateView(UpdateView):
    pk_url_kwarg = 'game_pk'
    form_class = GameUpdateForm
    template_name = "generic_game/game_update.html"
    
    def get_object(self, queryset=None):
        object = self.kwargs['game']
        self.extra_context = get_game_context(self.request, **self.kwargs)
        if not 'can_update' in self.extra_context:
            raise exceptions.PermissionDenied(_(u"You don''t have permissions to update game ''%(name)s''.") % {'name': object.name})
        return object
    
    def get_context_data(self, **kwargs):
        context = super(GameUpdateView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

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
        if character.master_id == request.user.id:
            context['can_update'] = True                 
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
    
    @method_decorator(permission_required('gamemanager.add_character'))
    def dispatch(self, *args, **kwargs):
        return super(CharacterCreateView, self).dispatch(*args, **kwargs)

class CharacterUpdateView(UpdateView):
    form_class = CharacterCreateForm
    template_name = "generic_game/character_update.html"
    
    def get_object(self, queryset=None):
        object = self.kwargs['character']
        self.extra_context = get_character_context(self.request, **self.kwargs)
        if not 'can_update' in self.extra_context:
            raise exceptions.PermissionDenied(_(u"You don''t have permissions to update character ''%(name)s''.") % {'name': object.name})
        return object
    
    def get_context_data(self, **kwargs):
        context = super(CharacterUpdateView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

class CharacterDetailView(DetailView):
    template_name = "generic_game/character_detail.html"
    
    def get_object(self, queryset=None):
        return self.kwargs['character']
    
    def get_context_data(self, **kwargs):
        context = super(CharacterDetailView, self).get_context_data(**kwargs)
        context.update(get_character_context(self.request, **self.kwargs))
        return context
