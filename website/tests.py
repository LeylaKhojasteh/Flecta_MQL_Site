from django.test import TestCase

from website.sitemaps import StaticViewSitemap


class SitemapTests(TestCase):
    def test_static_sitemap_uses_valid_home_route(self):
        self.assertEqual(
            StaticViewSitemap().items(),
            ['website:home', 'website:about', 'website:contact'],
        )
