from setuptools import setup

version = __import__('shopify_webhook').__version__

setup(
    name = 'django-shopify-webhook',
    version = version,
    description = 'A package for the creation of Shopify Apps using the Embedded App SDK.',
    long_description = open('README.rst').read(),
    author = 'Gavin Ballard',
    author_email = 'gavin@discolabs.com',
    url = 'https://github.com/discolabs/django-shopify-webhook',
    license = 'None',

    packages = [
        'shopify_webhook',
    ],

    package_dir = {
        'shopify_webhook': 'shopify_webhook',
    },

    install_requires = [
        'django >=1.6.5, <1.7',
    ],

    zip_safe = True,
    classifiers = [],
)