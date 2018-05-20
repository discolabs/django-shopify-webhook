from django.conf.urls import url
from ..views import WebhookView


urlpatterns = [
    url(r'webhook/', WebhookView.as_view(), name = 'webhook'),
]
