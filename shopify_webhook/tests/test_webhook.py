from django.dispatch import receiver

from ..signals import webhook_received, orders_create
from . import WebhookTestCase


class WebhookViewTestCase(WebhookTestCase):

    def test_get_method_not_allowed(self):
        response = self.client.get(self.webhook_url)
        self.assertEqual(response.status_code, 405, 'GET request returns 405 (Method Not Allowed).')

    def test_empty_post_message_is_bad_request(self):
        response = self.post_shopify_webhook()
        self.assertEqual(response.status_code, 400, 'Empty POST request returns 400 (Bad Request).')

    def test_no_hmac_is_forbidden(self):
        response = self.post_shopify_webhook(topic = 'orders/create', data = {'id': 123}, send_hmac = False)
        self.assertEqual(response.status_code, 403, 'POST orders/create request with no HMAC returns 403 (Forbidden).')

    def test_invalid_hmac_is_forbidden(self):
        response = self.post_shopify_webhook(topic = 'orders/create', data = {'id': 123}, headers = {'HTTP_X_SHOPIFY_HMAC_SHA256': 'invalid'}, send_hmac = False)
        self.assertEqual(response.status_code, 403, 'POST orders/create request with invalid HMAC returns 403 (Forbidden).')

    def test_unknown_topic_is_bad_request(self):
        response = self.post_shopify_webhook(topic = 'tests/invalid', data = {'id': 123})
        self.assertEqual(response.status_code, 400, 'POST tests/invalid request with valid HMAC returns 400 (Bad Request).')

    def test_missing_domain_is_bad_request(self):
        response = self.post_shopify_webhook(topic = 'orders/create', domain = '', data = {'id': 123})
        self.assertEqual(response.status_code, 400, 'POST orders/create request with missing domain returns 400 (Bad Request).')

    def test_valid_hmac_is_ok(self):
        response = self.post_shopify_webhook(topic = 'orders/create', data = {'id': 123})
        self.assertEqual(response.status_code, 200, 'POST orders/create request with valid HMAC returns 200 (OK).')

    def test_webook_received_signal_triggered(self):
        data = {'id': 123456}

        # Create a test signal receiver for the generic webhook received signal.
        @receiver(webhook_received)
        def test_webhook_received_receiver(sender, data, **kwargs):
            test_webhook_received_receiver.data = data
        test_webhook_received_receiver.data = None

        response = self.post_shopify_webhook(topic = 'fulfillments/update', data = data)
        self.assertEqual(data, test_webhook_received_receiver.data, 'POST fulfillments/update correctly triggered webhook_received signal.')

    def test_order_created_signal_triggered(self):
        data = {'id': 123456}

        # Create a test signal receiver for the order/created topic.
        @receiver(orders_create)
        def test_order_create_receiver(sender, data, **kwargs):
            test_order_create_receiver.data = data
        test_order_create_receiver.data = None

        response = self.post_shopify_webhook(topic = 'orders/create', data = data)
        self.assertEqual(data, test_order_create_receiver.data, 'POST orders/create correctly triggered order_created signal.')
