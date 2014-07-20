import logging

from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, HttpResponseBadRequest

from .decorators import webhook
import signals


class WebhookView(View):

    @method_decorator(csrf_exempt)
    @method_decorator(webhook)
    def post(self, request, *args, **kwargs):

        # Convert the topic to a signal name and trigger it.
        signal_name = request.webhook_topic.replace('/', '_')
        try:
            getattr(signals, signal_name).send_robust(self, data = request.webhook_data)
            signals.webhook_received.send_robust(self, data = request.webhook_data)
        except AttributeError:
            return HttpResponseBadRequest()

        # All good, return a 200.
        return HttpResponse('OK')