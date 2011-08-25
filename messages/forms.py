from django.forms import ModelForm
from .models import UserMessage

class MessageCreateForm(ModelForm):
    class Meta:
        model = UserMessage
        fields = ('receiver', 'subject', 'text', 'sent')
