import logging

from django.dispatch import Signal


class WebhookSignal(Signal):
    """A class wrapping Signal with the common arguments for Webhooks."""

    def __init__(self):
        providing_args = ['data']
        super(WebhookSignal, self).__init__(providing_args = providing_args)


# Define all of our Webhook signals.
app_uninstalled = WebhookSignal()
collections_create = WebhookSignal()
collections_update = WebhookSignal()
collections_delete = WebhookSignal()
order_created = WebhookSignal()