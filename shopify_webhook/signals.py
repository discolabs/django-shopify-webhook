from django.dispatch import Signal


class WebhookSignal(Signal):
    """
    A class wrapping Signal with the common arguments for Webhooks.
    """

    def __init__(self):
        providing_args = ['domain', 'topic', 'data']
        super(WebhookSignal, self).__init__(providing_args = providing_args)


# Define a generic webhook_received signal that triggers for all webhooks.
webhook_received = WebhookSignal()


# Define topic-specific signals.
orders_create = WebhookSignal()
orders_delete = WebhookSignal()
orders_updated = WebhookSignal()
orders_paid = WebhookSignal()
orders_cancelled = WebhookSignal()
orders_fulfilled = WebhookSignal()
orders_partially_fulfilled = WebhookSignal()
order_transactions_create = WebhookSignal()
carts_create = WebhookSignal()
carts_update = WebhookSignal()
checkouts_create = WebhookSignal()
checkouts_update = WebhookSignal()
checkouts_delete = WebhookSignal()
refunds_create = WebhookSignal()
products_create = WebhookSignal()
products_update = WebhookSignal()
products_delete = WebhookSignal()
collections_create = WebhookSignal()
collections_update = WebhookSignal()
collections_delete = WebhookSignal()
customer_groups_create = WebhookSignal()
customer_groups_update = WebhookSignal()
customer_groups_delete = WebhookSignal()
customers_create = WebhookSignal()
customers_enable = WebhookSignal()
customers_disable = WebhookSignal()
customers_update = WebhookSignal()
customers_delete = WebhookSignal()
fulfillments_create = WebhookSignal()
fulfillments_update = WebhookSignal()
shop_update = WebhookSignal()
disputes_create = WebhookSignal()
disputes_update = WebhookSignal()
app_uninstalled = WebhookSignal()
