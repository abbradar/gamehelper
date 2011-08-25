from django.conf.urls.defaults import patterns, url
from . import views

# todo: replace abs_url with reverse_lazy
urlpatterns = patterns('',
    url(r'received/$', views.MessageReceivedView.as_view(), name='message_received'),
    url(r'drafts/$', views.MessageDraftsView.as_view(), name='message_drafts'),
    url(r'sent/$', views.MessageSentView.as_view(), name='message_sent'),
    url(r'create/$', views.MessageCreateView.as_view(), name='message_create'),
    url(r'detail/(?P<pk>\d+)/$', views.MessageDetailView.as_view(), name='message_detail'),
    url(r'update/(?P<pk>\d+)/$', views.MessageUpdateView.as_view(), name='message_update'),
)
