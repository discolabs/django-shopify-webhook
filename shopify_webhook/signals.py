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
app_uninstalled = WebhookSignal()
carts_create = WebhookSignal()
carts_update = WebhookSignal()
checkouts_create = WebhookSignal()
checkouts_delete = WebhookSignal()
checkouts_update = WebhookSignal()
collection_listings_add = WebhookSignal()
collection_listings_remove = WebhookSignal()
collection_listings_update = WebhookSignal()
collections_create = WebhookSignal()
collections_delete = WebhookSignal()
collections_update = WebhookSignal()
customers_create = WebhookSignal()
customers_delete = WebhookSignal()
customers_disable = WebhookSignal()
customers_enable = WebhookSignal()
customers_update = WebhookSignal()
customer_groups_create = WebhookSignal()
customer_groups_delete = WebhookSignal()
customer_groups_update = WebhookSignal()
draft_orders_create = WebhookSignal()
draft_orders_delete = WebhookSignal()
draft_orders_update = WebhookSignal()
fulfillment_events_create = WebhookSignal()
fulfillment_events_delete = WebhookSignal()
fulfillments_create = WebhookSignal()
fulfillments_update = WebhookSignal()
inventory_items_create = WebhookSignal()
inventory_items_delete = WebhookSignal()
inventory_items_update = WebhookSignal()
inventory_levels_connect = WebhookSignal()
inventory_levels_disconnect = WebhookSignal()
inventory_levels_update = WebhookSignal()
locations_create = WebhookSignal()
locations_delet = WebhookSignal()
locations_update = WebhookSignal()
orders_cancelled = WebhookSignal()
orders_create = WebhookSignal()
orders_delete = WebhookSignal()
orders_fulfilled = WebhookSignal()
orders_paid = WebhookSignal()
orders_partially_fulfilled = WebhookSignal()
orders_updated = WebhookSignal()
order_transactions_create = WebhookSignal()
products_create = WebhookSignal()
products_delete = WebhookSignal()
products_update = WebhookSignal()
product_listings_add = WebhookSignal()
product_listings_remove = WebhookSignal()
product_listings_update = WebhookSignal()
refunds_create = WebhookSignal()
shop_update = WebhookSignal()
themes_create = WebhookSignal()
themes_delete = WebhookSignal()
themes_publish = WebhookSignal()
themes_update = WebhookSignal()
