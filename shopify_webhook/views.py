from django.views.generic import View, TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, HttpResponseBadRequest

from .decorators import webhook, app_proxy
from .helpers import get_signal_name_for_topic
import signals


class WebhookView(View):
    """
    A view to be used as the endpoint for webhook requests from Shopify.
    Accepts only the POST method and utilises the @webook view decorator to validate the request.
    """

    @method_decorator(csrf_exempt)
    @method_decorator(webhook)
    def post(self, request, *args, **kwargs):

        # Convert the topic to a signal name and trigger it.
        signal_name = get_signal_name_for_topic(request.webhook_topic)
        try:
            signals.webhook_received.send_robust(self, domain = request.webhook_domain, topic = request.webhook_topic, data = request.webhook_data)
            getattr(signals, signal_name).send_robust(self, domain = request.webhook_domain, topic = request.webhook_topic, data = request.webhook_data)
        except AttributeError:
            return HttpResponseBadRequest()

        # All good, return a 200.
        return HttpResponse('OK')


class LiquidTemplateView(TemplateView):
    """
    A view extending Django's base TemplateView that provides conveniences for returning a
    liquid-templated view from an app proxy request.
    """

    content_type = 'application/liquid; charset=utf-8'

    @method_decorator(app_proxy)
    def dispatch(self, request, *args, **kwargs):
        return super(LiquidTemplateView, self).dispatch(request, *args, **kwargs)
