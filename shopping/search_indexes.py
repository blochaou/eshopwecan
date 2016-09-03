from haystack import indexes
from .models import Product
from django.core.urlresolvers import reverse


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    slug = indexes.CharField(model_attr='slug',indexed=True)
    cat_slug = indexes.CharField(model_attr='categorie')
    uuid = indexes.CharField(model_attr='uuid',indexed=False)
    desc = indexes.CharField(model_attr='desc',indexed=True,default='')
    amazon_asin = indexes.CharField(model_attr='amazon_asin',indexed=False,default='')
    amazon_parent_asin = indexes.CharField(model_attr='amazon_parent_asin',indexed=False,null=True,default='')
    amazon_isbn = indexes.CharField(model_attr='amazon_isbn',indexed=False,null=True,default='')
    amazon_ean = indexes.CharField(model_attr='amazon_ean',indexed=False,null=True,default='')
    amazon_upc = indexes.CharField(model_attr='amazon_upc',indexed=False,null=True,default='')
    amazon_color = indexes.CharField(model_attr='amazon_color',indexed=False,null=True,default='')
    amazon_sku = indexes.CharField(model_attr='amazon_sku',indexed=False,null=True,default='')
    amazon_mpn = indexes.CharField(model_attr='amazon_mpn',indexed=False,null=True,default='')
    amazon_label = indexes.CharField(model_attr='amazon_label',indexed=False,null=True,default='')
    amazon_title = indexes.CharField(model_attr='amazon_title',indexed=False,default='')
    amazon_feature = indexes.CharField(model_attr='amazon_feature',indexed=True,null=True,default='')
    amazon_price = indexes.MultiValueField(model_attr="amazon_price")
    amazon_large_image_url = indexes.CharField(model_attr='amazon_large_image_url',indexed=False,null=True,default='')
    amazon_medium_image_url = indexes.CharField(model_attr='amazon_medium_image_url',indexed=False,null=True,default='')
    amazon_small_image_url = indexes.CharField(model_attr='amazon_small_image_url',indexed=False,null=True,default='')
    amazon_offer_url = indexes.CharField(model_attr='amazon_offer_url',indexed=False,null=True,default='')
    amazon_index = indexes.CharField(model_attr='amazon_index',indexed=False,null=True,default='')
    amazon_brand = indexes.CharField(model_attr='amazon_brand',indexed=False,null=True,default='')
    amazon_manufacturer = indexes.CharField(model_attr='amazon_manufacturer',indexed=False,null=True,default='')
    amazon_editorial_reviews = indexes.CharField(model_attr='amazon_editorial_reviews',indexed=False,null=True,default='')
    categorie =indexes.MultiValueField()
    is_index = indexes.BooleanField(model_attr='is_index',indexed=False,default='')
    date_creation = indexes.DateTimeField(model_attr='date_creation',indexed=False,default='')
    date_update = indexes.DateTimeField(model_attr='date_update',indexed=False,default='')
    get_absolute_url = indexes.CharField()

    def prepare_amazon_price(self, obj):
        return eval(obj.amazon_price)


    def prepare_cat_slug(self, obj):
        return  obj.categorie.slug

    def prepare_categorie(self,obj):
        return (obj.categorie.id,obj.categorie.slug,obj.categorie.name,obj.categorie.amazon_nodeid,obj.categorie.amazon_index)

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def prepare_date_creation(self,obj):
        return obj.date_creation.strftime('%Y-%m-%dT%H:%M:%SZ')

    def prepare_date_update(self,obj):
        return obj.date_update.strftime('%Y-%m-%dT%H:%M:%SZ')

    def prepare_get_absolute_url(self,obj):
        return reverse('shopping:products_details', args=[obj.categorie.slug, obj.slug])

