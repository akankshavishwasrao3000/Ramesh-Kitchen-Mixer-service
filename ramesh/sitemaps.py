from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class PublicPagesSitemap(Sitemap):
    protocol = "https"
    changefreq = "monthly"

    public_pages = (
        "index",
        "products",
        "services",
        "contact",
        "privacy_policy",
        "terms_conditions",
        "refund_policy",
        "shipping_policy",
    )

    def items(self):
        return self.public_pages

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == "index" else 0.7

    def get_domain(self, site=None):
        return "ramesh-kitchen-mixer-service-6fuw.onrender.com"
