import json

from django.test import TestCase
from django.conf import settings
from django.dispatch import receiver

from .signals import order_created
from .helpers import get_hmac


class WebhookViewTestCase(TestCase):

    def post_shopify_webhook(self, topic = None, data = {}, headers = {}, send_hmac = True):
        data = json.dumps(data)

        # Add common headers.
        headers['HTTP_X_SHOPIFY_TEST'] = 'true'

        # Add optional headers.
        if topic:
            headers['HTTP_X_SHOPIFY_TOPIC'] = topic
        if send_hmac:
            headers['HTTP_X_SHOPIFY_HMAC_SHA256'] = get_hmac(data, settings.SHOPIFY_APP_API_SECRET)

        return self.client.post('/webhook/', data = data, content_type = 'application/json', **headers)

    def test_get_method_not_allowed(self):
        response = self.client.get('/webhook/')
        self.assertEqual(response.status_code, 405, 'GET request returns 405 (Method Not Allowed).')

    def test_empty_post_message_is_bad_request(self):
        response = self.post_shopify_webhook()
        self.assertEqual(response.status_code, 400, 'Empty POST request returns 400 (Bad Request).')

    def test_no_hmac_is_forbidden(self):
        response = self.post_shopify_webhook(topic = 'order/created', data = {'id': 123}, send_hmac = False)
        self.assertEqual(response.status_code, 403, 'POST order/created request with no HMAC returns 403 (Forbidden).')

    def test_invalid_hmac_is_forbidden(self):
        response = self.post_shopify_webhook(topic = 'order/created', data = {'id': 123}, headers = {'HTTP_X_SHOPIFY_HMAC_SHA256': 'invalid'}, send_hmac = False)
        self.assertEqual(response.status_code, 403, 'POST order/created request with invalid HMAC returns 403 (Forbidden).')

    def test_valid_hmac_is_ok(self):
        response = self.post_shopify_webhook(topic = 'order/created', data = {'id': 123})
        self.assertEqual(response.status_code, 200, 'POST order/created request with valid HMAC returns 200 (OK).')

    def test_order_created_signal_triggered(self):
        data = {'id': 123456}

        # Create a test signal receiver for the order/created topic.
        @receiver(order_created)
        def test_order_created_receiver(sender, data, **kwargs):
            test_order_created_receiver.data = data
        test_order_created_receiver.data = None

        response = self.post_shopify_webhook(topic = 'order/created', data = data)
        self.assertEqual(data, test_order_created_receiver.data, 'POST order/created correctly triggered order_created signal.')