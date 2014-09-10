import os, sys
import json

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings

from ..helpers import get_hmac


class AbstractWebhookTestCase(TestCase):

    def setUp(self):
        super(AbstractWebhookTestCase, self).setUp()
        self.webhook_url = reverse('webhook')

    def post_shopify_webhook(self, topic = None, data = None, headers = None, send_hmac = True):
        # Set headers.
        headers = {} if headers is None else headers

        if isinstance(data, dict):
            data = json.dumps(data)
        elif data is None or not isinstance(data, basestring):
            data = '{}'

        # Add common headers.
        headers['HTTP_X_SHOPIFY_TEST'] = 'true'

        # Add optional headers.
        if topic:
            headers['HTTP_X_SHOPIFY_TOPIC'] = topic
        if send_hmac:
            headers['HTTP_X_SHOPIFY_HMAC_SHA256'] = get_hmac(data, settings.SHOPIFY_APP_API_SECRET)

        return self.client.post(self.webhook_url, data = data, content_type = 'application/json', **headers)

    def load_fixture(self, name, format = 'json'):
        fixture_path = "{0}/fixtures/{1}.{2}".format(os.path.dirname(sys.modules[self.__module__].__file__), name, format)
        with open(fixture_path, 'rb') as f:
            return f.read()
