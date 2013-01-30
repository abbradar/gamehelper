from django import forms
from .models import UserMessage, UserMessageCopy
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# This should be called only on non-sent messages
class UserMessageForm(forms.ModelForm):
  send = forms.BooleanField(label=_('Send'), required=False)

  class Meta:
    model = UserMessage
    queryset = UserMessage.objects.filter(sending_time=None)
    fields = ('receivers', 'subject', 'text')

  def __init__(self, *args, **kwargs):
    userid = kwargs.pop('userid', None)
    super(UserMessageForm, self).__init__(*args, **kwargs)

    if userid:
      self.fields['receivers'].queryset = User.objects.exclude(pk=userid)

  def clean(self):
    cleaned_data = super(UserMessageForm, self).clean()
    receivers = cleaned_data.get("receivers")
    sent = cleaned_data.get("sent")

    if sent and receivers:
      # Only do something if both fields are valid so far.
      if len(receivers) == 0:
        raise forms.ValidationError(_("Message should have at least one receiver when being sent."))

    # Always return the full collection of cleaned data.
    return cleaned_data
