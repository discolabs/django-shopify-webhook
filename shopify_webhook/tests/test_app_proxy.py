from django.test import TestCase
from django.test.client import RequestFactory
from django.http import HttpResponse, QueryDict
from django.utils.decorators import method_decorator

from ..decorators import app_proxy
from ..helpers import get_proxy_signature


class AppProxyTestCase(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()

    @method_decorator(app_proxy)
    def proxy_view(self, request, *args, **kwargs):
        return HttpResponse('OK')

    def get_proxy_request(self, signature = None):
        # Add common parameters to the request.
        data = {
            'extra': ['1', '2'],
            'shop': 'shop-name.myshopify.com',
            'path_prefix': '/apps/awesome_reviews',
            'timestamp': '1317327555'
        }

        if signature is not None:
            data['signature'] = signature

        request = self.request_factory.get('/proxy/', data = data)
        return request

    def test_signature_calculation(self):
        # Use the example provided in the Shopify documentation to verify our signature calculation works correctly.
        # See: http://docs.shopify.com/api/tutorials/application-proxies#security
        query_dict = QueryDict('extra=1&extra=2&shop=shop-name.myshopify.com&path_prefix=%2Fapps%2Fawesome_reviews&timestamp=1317327555')
        shared_secret = 'hush'
        expected_signature = 'a9718877bea71c2484f91608a7eaea1532bdf71f5c56825065fa4ccabe549ef3'
        calculated_signature = get_proxy_signature(query_dict, shared_secret)
        self.assertEqual(calculated_signature, expected_signature)

    def test_missing_signature_is_bad_request(self):
        request = self.get_proxy_request()
        response = self.proxy_view(request)
        self.assertEqual(response.status_code, 400)

    def test_invalid_signature_is_bad_request(self):
        request = self.get_proxy_request(signature = 'invalid')
        response = self.proxy_view(request)
        self.assertEqual(response.status_code, 400)

    def test_valid_signature_is_ok(self):
        request = self.get_proxy_request(signature = 'a9718877bea71c2484f91608a7eaea1532bdf71f5c56825065fa4ccabe549ef3')
        response = self.proxy_view(request)
        self.assertEqual(response.status_code, 200)