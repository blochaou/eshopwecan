from django.contrib.sitemaps import Sitemap
from .models import Product,Word

class ProductSitemap(Sitemap):

    def items(self):
        return Product.objects.all()

class WordSitemap(Sitemap):
    def items(self):
        return Word.objects.all()
