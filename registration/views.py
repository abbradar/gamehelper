from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.conf import settings

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            if request.POST['next']:
              return HttpResponseRedirect(request.POST['next'])
            else:
              return HttpResponseRedirect('/accounts/profile/')
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {'form': form}, context_instance=RequestContext(request))

def profile(request, object_id=None):
    if object_id is None:
      if not request.user.is_authenticated():
        return HttpResponseRedirect(settings.LOGIN_URL)
      return render_to_response("registration/profile.html", {'object': request.user}, context_instance=RequestContext(request))
    else:
      try:
        return render_to_response("registration/profile.html", {'object': User.objects.get(id=object_id)}, context_instance=RequestContext(request))
      except User.DoesNotExist:
        return HttpResponseRedirect('/')
