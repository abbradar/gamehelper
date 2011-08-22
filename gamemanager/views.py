from django.views.generic import FormView, ListView, DetailView, UpdateView, CreateView
from django.views.generic.edit import FormMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core import exceptions
from django.http import HttpResponseRedirect, Http404
from django.utils.translation import ugettext as _
from django.core.urlresolvers import get_callable
from . import models
from .game_types import GameTypeForm, game_types
from .game_views import get_game_context, get_character_context
from misc.urlresolvers import DynamicURLResolver

class GameListView(ListView):
    template_name = "gamemanager/game_list.html"
    model = models.Game

    def get_context_data(self, **kwargs):
        context = super(GameListView, self).get_context_data(**kwargs)
        if self.request.user.has_perm('gamemanager.create_game'):
            context['can_create'] = True
        return context

class CharacterListView(ListView):
    template_name = "gamemanager/character_list.html"
    
    def get_queryset(self):
        if self.kwargs['pk'] == 'me':
            if not self.request.user.is_authenticated():
                # TODO: redirect to login page instead
                raise exceptions.PermissionDenied('You need to login to view your own characters list.')
            self.current_user = self.request.user
        else:
            self.current_user = get_object_or_404(User, id=self.kwargs['pk'])
        return models.Character.objects.filter(master=self.current_user.id)

    def get_context_data(self, **kwargs):
        context = super(CharacterListView, self).get_context_data(**kwargs)
        context['current_user'] = self.current_user
        if self.request.user.has_perm('gamemanager.create_character'):
            context['can_create'] = True
        return context

class GameTypeView(FormView):
    form_class = GameTypeForm
    type_field_name = 'type'
    
    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url() % {self.type_field_name: form.cleaned_data['type']})

class GameCreateTypeView(GameTypeView):
    template_name = 'gamemanager/game_create.html'   
    
    @method_decorator(permission_required('gamemanager.create_game'))
    def dispatch(self, *args, **kwargs):
        return super(GameTypeView, self).dispatch(*args, **kwargs)

class CharacterCreateTypeView(GameTypeView):
    template_name = 'gamemanager/character_create.html'   
    
    @method_decorator(permission_required('gamemanager.create_character'))
    def dispatch(self, *args, **kwargs):
        return super(GameTypeView, self).dispatch(*args, **kwargs)

class GameTypeFormView(CreateView):
    game_type_field_name = 'type'
    
    def get_form_class(self):
        if self.form_name is '':
            raise exceptions.ImproperlyConfigured("Provide form name")
        try:
            self.game_type = self.kwargs[self.game_type_field_name]
        except KeyError:
            raise exceptions.ImproperlyConfigured('No game type to load form. Please, specify game type.')
        try:
            return getattr(game_types.classes[self.game_type], self.form_name)
        except KeyError:
            raise Http404(_(u"Game type %(game_type)s is invalid.") % {'game_type': self.game_type})

class GameCreateView(GameTypeFormView):
    template_name = 'gamemanager/game_create.html'
    form_name = 'game_create_form'
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.type = self.game_type
        self.object.save()
        gm = models.GameMaster(master = self.request.user, game = self.object)
        gm.save()
        return FormMixin.form_valid(self, form)
    
    @method_decorator(permission_required('gamemanager.create_game'))
    def dispatch(self, *args, **kwargs):
        return super(GameCreateView, self).dispatch(*args, **kwargs)

class CharacterCreateView(GameTypeFormView):
    template_name = 'gamemanager/character_create.html'
    form_name = 'character_create_form'
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.type = self.game_type
        self.object.master = self.request.user
        self.object.save()
        return FormMixin.form_valid(self, form)
    
    @method_decorator(permission_required('gamemanager.create_character'))
    def dispatch(self, *args, **kwargs):
        return super(CharacterCreateView, self).dispatch(*args, **kwargs)

class ByTypeDetailView(DynamicURLResolver):
    def get_urls(self, name):
        urls = self.get_type_urls(name)
        if isinstance(urls, tuple):
            urls, self.default_view = urls
        return urls
    
    def get_default_view(self):
        urls = self.get_urls(self.get_name())
        return super(ByTypeDetailView, self).get_default_view()

class GameDetailView(ByTypeDetailView):
    def get_name(self):
        game = get_object_or_404(models.Game, id=self.kwargs['game_pk'])
        self.extra_kwargs['game'] = game
        return game.type
    
    def get_extra_kwargs(self):
        self.extra_kwargs['game_pk'] = self.kwargs['game_pk']
        return super(GameDetailView, self).get_extra_kwargs()
    
    def get_type_urls(self, name):
        return game_types.classes[name].game_urls

class CharacterDetailView(ByTypeDetailView):
    def get_name(self):
        character = get_object_or_404(models.Character, id=self.kwargs['char_pk'])
        self.extra_kwargs['character'] = character
        return character.type
    
    def get_extra_kwargs(self):
        self.extra_kwargs['char_pk'] = self.kwargs['char_pk']
        return super(CharacterDetailView, self).get_extra_kwargs()
    
    def get_type_urls(self, name):
        return game_types.classes[name].character_urls

class GameUpdateView(UpdateView):
    template_name = "gamemanager/game_update.html"
    model = models.Game
    pk_url_kwarg = 'game_pk'
    
    def get_form_class(self):
        game_type = self.object.type
        form_class = game_types.classes[game_type].game_update_form
        model = form_class.Meta.model
        # It should be better to convert existing object to extended one, but I have no idea how can I.
        if not isinstance(self.object, model):
            self.object = model.objects.get(id=self.object.id)
        return form_class
    
    def get_object(self, queryset=None):
        object = super(CharacterUpdateView, self).get_object(queryset)    
        self.game_context = get_game_context(self.request, game=object, **self.kwargs)
        if not 'my_gm' in self.game_context:
            if not self.request.user.has_perm('gamemanager.update_game'):
                raise exceptions.PermissionDenied(_(u"You don''t have permissions to update game ''%(name)s''.") % {'name': object.name})
        return object
    
    def get_context_data(self, **kwargs):
        context = super(GameUpdateView, self).get_context_data(**kwargs)
        context.update(self.game_context)
        return context

class CharacterUpdateView(UpdateView):
    template_name = "gamemanager/character_update.html"
    model = models.Character
    pk_url_kwarg = 'char_pk'
    
    def get_form_class(self):
        game_type = self.object.type
        form_class = game_types.classes[game_type].character_update_form
        model = form_class.Meta.model
        # It should be better to convert existing object to extended one, but I have no idea how can I.
        if not isinstance(self.object, model):
            self.object = model.objects.get(id=self.object.id)
        return form_class
    
    def get_object(self, queryset=None):
        object = super(CharacterUpdateView, self).get_object(queryset)
        if object.master_id != self.request.user.id:
            if not self.request.user.has_perm('gamemanager.update_character'):
                raise exceptions.PermissionDenied(_(u"You don''t have permissions to update character ''%(name)s''.") % {'name': object.name})
        return object
    
    def get_context_data(self, **kwargs):
        context = super(CharacterUpdateView, self).get_context_data(**kwargs)
        context.update(get_character_context(self.request, character=self.object, **self.kwargs))
        return context
