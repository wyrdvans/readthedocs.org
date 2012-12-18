from django.http import Http404
from django.core.cache import cache
from django.conf import settings
from django.utils import unittest
from django.test.client import RequestFactory
from django.test.utils import override_settings

from readthedocs.core.middleware import SubdomainMiddleware

class MiddlewareTests(unittest.TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SubdomainMiddleware()
        self.url = '/'

    def test_failey_cname(self):
        request = self.factory.get(self.url, HTTP_HOST = 'my.host.com')
        with self.assertRaises(Http404):
            ret_val = self.middleware.process_request(request)
        self.assertEqual(request.cname, True)

    def test_proper_subdomain(self):
        request = self.factory.get(self.url, HTTP_HOST = 'pip.readthedocs.org')
        ret_val = self.middleware.process_request(request)
        self.assertEqual(request.urlconf, 'core.subdomain_urls')
        self.assertEqual(request.subdomain, True)
        self.assertEqual(request.slug, 'pip')


    def test_proper_cname(self):
        cache.get = lambda x: 'my_slug'
        request = self.factory.get(self.url, HTTP_HOST = 'my.valid.homename')
        ret_val = self.middleware.process_request(request)
        self.assertEqual(request.urlconf, 'core.subdomain_urls')
        self.assertEqual(request.cname, True)
        self.assertEqual(request.slug, 'my_slug')

    def test_djangome(self):
        request = self.factory.get(self.url, HTTP_HOST = 'pip.rtfd.org')
        ret_val = self.middleware.process_request(request)
        self.assertEqual(request.urlconf, 'core.djangome_urls')
        self.assertEqual(request.slug, 'pip')
        self.assertFalse(hasattr(request, 'subdomain'))

    @override_settings(DEBUG=True)
    def test_debug_on(self):
        request = self.factory.get(self.url, HTTP_HOST = 'doesnt.really.matter')
        ret_val = self.middleware.process_request(request)
        self.assertEqual(ret_val, None)
