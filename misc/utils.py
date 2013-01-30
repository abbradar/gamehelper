"""
All kinds of functions which don't fit into other modules.
"""

from django.utils.importlib import import_module
from django.utils.functional import SimpleLazyObject, new_method_proxy
from django.core import exceptions

class LazyList(SimpleLazyObject):
  """
  List which populates itself from populate() callable when accessed first time.
  """
  
  def __init__(self, populate, *args, **kvargs):
    super(LazyList, self).__init__()
    self._populate = populate
    self._args = args
    self._kvargs = kvargs
  
  def _setup(self):
    self._wrapped = self._populate(*self._args, **self._kvargs)
  
  def __setattr__(self, name, value):
    if name in ('_populate', '_wrapped', '_args', '_kvargs'):
      self.__dict__[name] = value
    else:
      if self._wrapped is empty:
        self._setup()
      setattr(self._wrapped, name, value)

  __iter__ = new_method_proxy(iter)

def get_class(name):
  try:
    module, classname = name.rsplit('.', 1)
  except ValueError:
    try:
      mod = import_module(".")
      return getattr(mod, classname)
    except AttributeError:
      raise exceptions.ImproperlyConfigured('%s isn\'t a valid class address' % name)
  try:
    mod = import_module(module)
  except ImportError, e:
    raise exceptions.ImproperlyConfigured('Error importing module %s: "%s"' % (module, e))
  try:
    return getattr(mod, classname)
  except AttributeError:
    raise exceptions.ImproperlyConfigured('Module "%s" does not define a "%s" class' % (module, classname))
