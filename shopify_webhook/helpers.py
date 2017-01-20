from django.conf import settings
import hashlib, base64, hmac


def get_signal_name_for_topic(webhook_topic):
    """
    Convert a Shopify Webhook topic (eg "orders/create") to the equivalent Pythonic method name (eg "orders_create").
    """
    return webhook_topic.replace('/', '_')


def domain_is_valid(domain):
    """
    Check whether the given domain is a valid source for webhook request.
    """
    if domain is None:
        return False
    return len(domain) > 0


def get_hmac(body, secret):
    """
    Calculate the HMAC value of the given request body and secret as per Shopify's documentation for Webhook requests.
    See: http://docs.shopify.com/api/tutorials/using-webhooks#verify-webhook
    """
    hash = hmac.new(secret.encode('utf-8'), body, hashlib.sha256)
    return base64.b64encode(hash.digest()).decode()


def hmac_is_valid(body, secret, hmac_to_verify):
    """
    Return True if the given hmac_to_verify matches that calculated from the given body and secret.
    """
    return get_hmac(body, secret) == hmac_to_verify


def get_proxy_signature(query_dict, secret):
    """
    Calculate the signature of the given query dict as per Shopify's documentation for proxy requests.
    See: http://docs.shopify.com/api/tutorials/application-proxies#security
    """

    # Sort and combine query parameters into a single string.
    sorted_params = ''
    for key in sorted(query_dict.keys()):
        sorted_params += "{0}={1}".format(key, ",".join(query_dict.getlist(key)))

    signature = hmac.new(secret.encode('utf-8'), sorted_params.encode('utf-8'), hashlib.sha256)
    return signature.hexdigest()


def proxy_signature_is_valid(request, secret):
    """
    Return true if the calculated signature matches that present in the query string of the given request.
    """

    # Allow skipping of validation with an explicit setting.
    # If setting not present, skip if in debug mode by default.
    skip_validation = getattr(settings, 'SKIP_APP_PROXY_VALIDATION', settings.DEBUG)
    if skip_validation:
        return True

    # Create a mutable version of the GET parameters.
    query_dict = request.GET.copy()

    # Extract the signature we're going to verify. If no signature's present, the request is invalid.
    try:
        signature_to_verify = query_dict.pop('signature')[0]
    except KeyError:
        return False

    calculated_signature = get_proxy_signature(query_dict, secret)

    # Try to use compare_digest() to reduce vulnerability to timing attacks.
    # If it's not available, just fall back to regular string comparison.
    try:
        return hmac.compare_digest(calculated_signature.encode('utf-8'), signature_to_verify.encode('utf-8'))
    except AttributeError:
        return calculated_signature == signature_to_verify
