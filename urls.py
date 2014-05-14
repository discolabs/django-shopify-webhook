from django.conf.urls import patterns, url
from .views import WebhookView


urlpatterns = patterns('',
    url(r'^$', WebhookView.as_view(), name = 'webhook'),
)