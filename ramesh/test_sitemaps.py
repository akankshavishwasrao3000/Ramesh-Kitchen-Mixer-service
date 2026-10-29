from xml.etree import ElementTree

from django.test import SimpleTestCase


class SitemapTests(SimpleTestCase):
    def test_sitemap_lists_only_canonical_public_pages(self):
        response = self.client.get("/sitemap.xml")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("application/xml"))

        root = ElementTree.fromstring(response.content)
        namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        locations = {
            node.text
            for node in root.findall(f"{namespace}url/{namespace}loc")
        }

        self.assertEqual(
            locations,
            {
                "https://ramesh-kitchen-mixer-service-6fuw.onrender.com/",
                "https://ramesh-kitchen-mixer-service-6fuw.onrender.com/products/",
                "https://ramesh-kitchen-mixer-service-6fuw.onrender.com/services/",
                "https://ramesh-kitchen-mixer-service-6fuw.onrender.com/contact/",
                "https://ramesh-kitchen-mixer-service-6fuw.onrender.com/privacy-policy/",
                "https://ramesh-kitchen-mixer-service-6fuw.onrender.com/terms-and-conditions/",
                "https://ramesh-kitchen-mixer-service-6fuw.onrender.com/refund-policy/",
                "https://ramesh-kitchen-mixer-service-6fuw.onrender.com/shipping-policy/",
            },
        )

    def test_robots_txt_references_the_canonical_sitemap(self):
        response = self.client.get("/robots.txt")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("text/plain"))
        self.assertIn(
            "Sitemap: https://ramesh-kitchen-mixer-service-6fuw.onrender.com/sitemap.xml",
            response.content.decode(),
        )
