from django.views.generic import View
from django.utils.functional import memoize
from django.core.urlresolvers import RegexURLResolver
from django.conf.urls.defaults import include
from django.core import exceptions

class DynamicViewMixin(object):
  def dispatch(self, request, *args, **kwargs):
    self.request = request
    self.args = args
    self.kwargs = kwargs
    return self.handler()
  
  def handler(self):
    view = self.get_view()
    args, kwargs = self.get_args()
    return view(self.request, *args, **kwargs)
  
  def get_args(self):
    return self.args, self.kwargs

class DynamicView(DynamicViewMixin, View):
  def __init__(self, **kwargs):
    super(DynamicView, self).__init__(**kwargs)

# Here goes ugly thing that uses Django internal API
# to dynamically resolve URLs based on game type.
# To be rewritten with pure Django public API if it
# supports such tricks in the future.
# TODO: as of now it raises "It Worked!" page instead of normal debug
# page when DEBUG=True and no URLs configured
class DynamicResolveView(DynamicView):
  def __init__(self, **kwargs):
    super(DynamicResolveView, self).__init__(**kwargs)
    self._cache = {}
  
  def get_resolver(self, name):
    def _wrapped(name):
      urls = self.get_urls(name)
      urlconf_module, app_name, namespace = include(urls)
      resolver = RegexURLResolver('', urlconf_module, {}, app_name=app_name, namespace=namespace)
      return resolver
    _wrapped = memoize(_wrapped, self._cache, 1)
    return _wrapped(name)
  
  def get_path(self):
    if 'path' in self.kwargs:
      return self.kwargs['path']
    else:
      raise exceptions.ImproperlyConfigured('Path is not set')
  
  def get_view(self):
    resolver = self.get_resolver(self.get_name())
    view, args, kwargs = resolver.resolve(self.get_path())
    self._view_args = args
    self._view_kwargs = kwargs
    return view
  
  def get_args(self):
    return self._view_args, self._view_kwargs
