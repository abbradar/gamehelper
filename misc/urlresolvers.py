from django.views.generic import View
from django.utils.functional import memoize
from django.core.urlresolvers import RegexURLResolver
from django.conf.urls.defaults import include
from django.core import exceptions

# Here goes ugly thing that uses Django internal API
# to dynamically resolve URLs based on game type.
# To be rewritten with pure Django public API if it
# supports such tricks in the future.
# TODO: as of now it raises "It Worked!" page instead of normal debug
# page when DEBUG=True and no URLs configured
class DynamicURLResolver(View):
    _cache = {}
    default = False
    default_view = None
    extra_kwargs = {}
    
    def get_resolver(self):
        def _wrapped(name):
            urls = self.get_urls(name)
            urlconf_module, app_name, namespace = include(urls)
            resolver = RegexURLResolver('', urlconf_module, {}, app_name=app_name, namespace=namespace)
            return resolver
        
        _wrapped = memoize(_wrapped, self._cache, 1)        
        return _wrapped(self.get_name())
    
    def get_default_view(self):
        if self.default_view:
            return self.default_view
        else:
            raise exceptions.ImproperlyConfigured('Default view is not declared')
    
    def get_path(self):
        if 'path' in self.kwargs:
            return self.kwargs['path']
        else:
            raise exceptions.ImproperlyConfigured('Path is not set')
    
    def get_extra_kwargs(self):
        return self.extra_kwargs
            
    def get(self, *args, **kwargs):
        if self.default:
            view = self.get_default_view()
            view_args = []
            view_kwargs = {}
        else:
            view, view_args, view_kwargs = self.get_resolver().resolve(self.get_path())
        view_kwargs.update(self.get_extra_kwargs())
        return view(self.request, *view_args, **view_kwargs)
    
    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    # PUT is a valid HTTP verb for creating (with a known URL) or editing an
    # object, note that browsers only support POST for now.
    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)
