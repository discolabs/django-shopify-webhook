import json
from functools import wraps

from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.conf import settings

from .helpers import hmac_is_valid


def webhook(f):
  """A decorator thats check and validates a Shopify Webhook request."""

  @wraps(f)
  def wrapper(request, *args, **kwargs):
    # Try to get required headers and decode the body of the request.
    try:
      topic = request.META['HTTP_X_SHOPIFY_TOPIC']
      hmac  = request.META['HTTP_X_SHOPIFY_HMAC_SHA256'] if 'HTTP_X_SHOPIFY_HMAC_SHA256' in request.META else None
      data  = json.loads(request.body)
    except:
      return HttpResponseBadRequest()

    # Verify the HMAC.
    if not hmac_is_valid(request.body, settings.SHOPIFY_APP_API_SECRET, hmac):
      return HttpResponseForbidden()

    # Otherwise, set properties on the request object and return.
    request.webhook_topic = topic
    request.webhook_data  = data
    return f(request, args, kwargs)

  return wrapper