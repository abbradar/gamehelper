from django.views.generic import View, FormView, ListView, DeleteView
from django.views.generic.edit import FormMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core import exceptions
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import get_callable
from django.utils.translation import ugettext as _
from . import models
from .game_types import GameTypeForm, game_types
from misc.views import DynamicView, DynamicResolveView

class GameListView(ListView):
    template_name = "games/game_list.html"
    model = models.Game

    def get_context_data(self, **kwargs):
        context = super(GameListView, self).get_context_data(**kwargs)
        if self.request.user.has_perm('games.add_game'):
            context['can_create'] = True
        return context

class CharacterListView(ListView):
    template_name = "games/character_list.html"
    model = models.Character
    
    def get_queryset(self):
        if self.kwargs['pk'] == 'me':
            if not self.request.user.is_authenticated():
                # TODO: redirect to login page instead
                raise exceptions.PermissionDenied('You need to login to view your own characters list.')
            self.current_user = self.request.user
        else:
            self.current_user = get_object_or_404(User, id=self.kwargs['pk'])
        return self.model.objects.filter(master=self.current_user.id)

    def get_context_data(self, **kwargs):
        context = super(CharacterListView, self).get_context_data(**kwargs)
        context['current_user'] = self.current_user
        if self.request.user.has_perm('games.add_character'):
            context['can_create'] = True
        return context

class GameTypeView(FormView):
    form_class = GameTypeForm
    type_field_name = 'type'
    
    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url() % {self.type_field_name: form.cleaned_data['type']})

class GameCreateTypeView(GameTypeView):
    template_name = 'games/game_type.html'   
    
    @method_decorator(permission_required('games.add_game'))
    def dispatch(self, *args, **kwargs):
        return super(GameTypeView, self).dispatch(*args, **kwargs)

class CharacterCreateTypeView(GameTypeView):
    template_name = 'games/character_type.html'   
    
    @method_decorator(permission_required('games.add_character'))
    def dispatch(self, *args, **kwargs):
        return super(GameTypeView, self).dispatch(*args, **kwargs)

class TypeBasedView(DynamicView):
    def get_view(self):
        self.type = self.get_type()
        type_class = game_types.classes[self.type]
        view = getattr(type_class, self.view_field)
        view = get_callable(view)
        return view
    
    def get_args(self):
        args, kwargs = super(TypeBasedView, self).get_args()
        kwargs['type'] = self.type
        return args, kwargs

class GameCreateView(TypeBasedView):
    view_field = 'game_create_view'
    type_field_name = 'type'
    
    def get_type(self):
        return self.kwargs[self.type_field_name]
    
    @method_decorator(permission_required('games.add_game'))
    def dispatch(self, *args, **kwargs):
        return super(GameCreateView, self).dispatch(*args, **kwargs)

class CharacterCreateView(TypeBasedView):
    view_field = 'character_create_view'
    type_field_name = 'type'
    
    def get_type(self):
        return self.kwargs[self.type_field_name]
    
    @method_decorator(permission_required('games.add_character'))
    def dispatch(self, *args, **kwargs):
        return super(CharacterCreateView, self).dispatch(*args, **kwargs)

class GameUpdateView(TypeBasedView):
    view_field = 'game_update_view'
    
    def get_type(self):
        self.game = get_object_or_404(models.Game, id=self.kwargs['game_pk'])
        try:
            self.gm = models.GameMaster.objects.get(master=self.request.user, game=self.game)
        except exceptions.ObjectDoesNotExist:
            if not self.request.user.has_perm('games.change_game'):
                raise exceptions.PermissionDenied(_(u"You don''t have permissions to update game ''%(name)s''.") % {'name': object.name})            
        return self.game.type
    
    def get_args(self):
        args, kwargs = super(GameUpdateView, self).get_args()
        kwargs['game'] = self.game
        kwargs['gm'] = self.gm
        return args, kwargs
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GameUpdateView, self).dispatch(*args, **kwargs)

class CharacterUpdateView(TypeBasedView):
    view_field = 'character_update_view'
    
    def get_type(self):
        self.character = get_object_or_404(models.Character, id=self.kwargs['char_pk'])
        if not self.character.master != self.request.user:
            if not self.request.user.has_perm('games.change_character'):
                raise exceptions.PermissionDenied(_(u"You don''t have permissions to update character ''%(name)s''.") % {'name': object.name})
        return self.game.type
        return self.character.type
    
    def get_args(self):
        args, kwargs = super(CharacterUpdateView, self).get_args()
        kwargs['character'] = self.character
        return args, kwargs
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CharacterUpdateView, self).dispatch(*args, **kwargs)

class GameDeleteView(DeleteView):
    template_name = 'games/game_confirm_delete.html'
    model = models.Game
    
    def get_object(self, queryset=None):
        object = super(GameDeleteView, self).get_object(queryset)
        try:
            game_masters.get(master=self.request.user.id, game=object.id)
        except exceptions.ObjectDoesNotExist:
            if not self.request.user.has_perm('games.delete_game'):
                raise exceptions.PermissionDenied(_(u"You don''t have permissions to delete game ''%(name)s''.") % {'name': object.name})
        return object
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GameDeleteView, self).dispatch(*args, **kwargs)

class CharacterDeleteView(DeleteView):
    template_name = 'games/character_confirm_delete.html'
    model = models.Character
    
    def get_object(self, queryset=None):
        object = super(CharacterDeleteView, self).get_object(queryset)
        if object.master != request.user:
            if not request.user.has_perm('games.delete_character'):            
                raise exceptions.PermissionDenied(_(u"You don''t have permissions to delete character ''%(name)s''.") % {'name': object.name})
        return object
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CharacterDeleteView, self).dispatch(*args, **kwargs)

class GameDetailView(DynamicResolveView):
    def get_name(self):
        self.game = get_object_or_404(models.Game, id=self.kwargs['game_pk'])
        return self.game.type
    
    def get_args(self):
        args, kwargs = super(GameDetailView, self).get_args()
        kwargs['game'] = self.game
        return args, kwargs
    
    def get_urls(self, name):
        return game_types.classes[name].game_urls

class CharacterDetailView(DynamicResolveView):
    def get_name(self):
        self.character = get_object_or_404(models.Character, id=self.kwargs['char_pk'])
        return self.character.type
    
    def get_args(self):
        args, kwargs = super(CharacterDetailView, self).get_args()
        kwargs['character'] = self.character
        return args, kwargs
    
    def get_urls(self, name):
        return game_types.classes[name].character_urls

game_detail_view = GameDetailView()
character_detail_view = CharacterDetailView()
