from django.template import RequestContext, loader
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden

class Http403Middleware(object):
  def process_exception(self, request, exception):
    if isinstance(exception, PermissionDenied):
      if not settings.DEBUG:
        return HttpResponseForbidden(loader.render_to_string('403.html', context_instance=RequestContext(request)))
