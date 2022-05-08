Django Shopify Webhook
======================

[![PyPI version](https://badge.fury.io/py/django-shopify-webhook.svg)](http://badge.fury.io/py/django-shopify-webhook)
[![Tests](https://github.com/discolabs/django-shopify-webhook/actions/workflows/ci.yml/badge.svg)](https://github.com/discolabs/django-shopify-webhook/actions/workflows/ci.yml)

This Django package aims to make it easy to add webhook-handling behaviour into
your Django app. It provides:

- A `WebhookView` for catching and verifying webhooks sent from Shopify, and
  triggering the appropriate webhook signal.
  
- `webhook`, `carrier_request` and `app_proxy` view decorators that validate
  these various types of request.
  
- A number of `WebhookSignal`s that can be listened to and handled by your
  application.

This packaged is maintained by [Josef Rousek](https://rousek.name/) from [Digismoothie](https://digismoothie.com/) and yes, we're hiring.
