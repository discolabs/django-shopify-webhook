import os, sys
import json

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import six

from ..helpers import get_hmac


class WebhookTestCase(TestCase):
    """
    A base class for running tests on Shopify webhooks. Can be used by `shopify_webhook` tests here, or by other
    packages that utilise webhook behaviour.
    """

    def setUp(self):
        """
        Set up the test case, primarily by getting a reference to the webhook endpoint to be used for testing.
        """
        super(WebhookTestCase, self).setUp()
        self.webhook_url = reverse('webhook')

    def post_shopify_webhook(self, topic = None, domain = None, data = None, headers = None, send_hmac = True):
        """
        Simulate a webhook being sent to the application's webhook endpoint with the provided parameters.
        """
        # Set defaults.
        domain = 'test.myshopify.com' if domain is None else domain
        data = {} if data is None else data
        headers = {} if headers is None else headers

        # Dump data as a JSON string.
        data = json.dumps(data)

        # Add required headers.
        headers['HTTP_X_SHOPIFY_TEST'] = 'true'
        headers['HTTP_X_SHOPIFY_SHOP_DOMAIN'] = domain

        # Add optional headers.
        if topic:
            headers['HTTP_X_SHOPIFY_TOPIC'] = topic
        if send_hmac:
            headers['HTTP_X_SHOPIFY_HMAC_SHA256'] = six.text_type(get_hmac(six.b(data), settings.SHOPIFY_WEBHOOK_SECRET))

        return self.client.post(self.webhook_url, data = data, content_type = 'application/json', **headers)

    def read_fixture(self, name):
        """
        Read a .json fixture with the specified name, parse it as JSON and return.
        Currently makes the assumption that a directory named 'fixtures' containing .json files exists and is located
        in the same directory as the file running the tests.
        """
        fixture_path = "{0}/fixtures/{1}.json".format(os.path.dirname(sys.modules[self.__module__].__file__), name, format)
        with open(fixture_path, 'rb') as f:
            return json.loads(f.read())
