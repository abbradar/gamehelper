from django.views.generic import FormView, ListView, DetailView, UpdateView, CreateView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.detail import SingleObjectMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.core import exceptions
from django.http import HttpResponseRedirect, Http404
from django.utils.translation import ugettext as _
from . import models
from .game_types import GameTypeForm, game_types
from .game_views import get_game_context
from django.conf.urls.defaults import include
from django.core.urlresolvers import RegexURLResolver

class GameListView(ListView):
    template_name = "gamemanager/game_list.html"
    model = models.Game

    def get_context_data(self, **kwargs):
        context = super(GameListView, self).get_context_data(**kwargs)
        if self.request.user.has_perm('gamemanager.create_game'):
            context['can_create'] = True
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
            self.game_type = self.kwargs[self.game_type_field_name]
        except KeyError:
            raise exceptions.ImproperlyConfigured('No game type to load form. Please, specify game type.')
        try:
            return game_types.classes[self.game_type].game_create_form
        except KeyError:
            raise Http404(_(u"Game type %(game_type)s is invalid.") % {'game_type': self.game_type})
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.type = self.game_type
        self.object.save()
        gm = models.GameMaster(master = self.request.user, game = self.object)
        gm.save()
        return super(ModelFormMixin, self).form_valid(form)
    
    @method_decorator(permission_required('gamemanager.create_game'))
    def dispatch(self, *args, **kwargs):
        return super(GameCreateView, self).dispatch(*args, **kwargs)

def game_detail_view(request, game_pk, *args, **kwargs):
    game = models.Game.objects.get(id=game_pk)
    view = game_types.classes[game.type].default_view
    return view(request, game=game, game_pk=game_pk, *args, **kwargs)

# Here goes ugly thing that uses Django internal API
# to dynamically resolve URLs based on game type.
# To be rewritten with pure Django public API if it
# supports such tricks in the future.
# TODO: as of now it raises "It Worked!" page instead of normal debug
# page when DEBUG=True and no URLs configured
def game_resolve_view(request, regex, game_pk, **kwargs):
    game = models.Game.objects.get(id=game_pk)
    urls = game_types.classes[game.type].urls
    urlconf_module, app_name, namespace = include(urls)
    resolver = RegexURLResolver('', urlconf_module, kwargs, app_name=app_name, namespace=namespace)
    view, view_args, view_kwargs = resolver.resolve(regex)
    return view(*view_args, **view_kwargs)

class GameUpdateView(UpdateView):
    template_name = "gamemanager/game_update.html"
    
    def get_form_class(self):
        game_type = self.object.type
        return game_types.classes[game_type].game_update_form
    
    def get_object(self, queryset=None):
        self.game_context = get_game_context(self.request, **self.kwargs)
        if not 'my_gm' in self.game_context:
            if not self.request.user.has_perm('gamemanager.update_game'):
                raise exceptions.PermissionDenied(_(u"You don''t have permissions to update game ''%(game)s''.") % {'game': self.game_context['game'].name})
        return self.game_context['game']
    
    def get_context_data(self, **kwargs):
        context = super(GameUpdateView, self).get_context_data(**kwargs)
        context.update(self.game_context)
        return context
