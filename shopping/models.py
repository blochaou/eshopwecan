from django.db import models
from django.utils.text import slugify
from stdimage.models import StdImageField
from stdimage.utils import UploadToAutoSlug
from django.core.urlresolvers import reverse
import os
import uuid
from eshopwecan import settings


def upload_path(instance,filename):
    return os.path.join('static/images',str(instance.slug)+"-"+str(uuid.uuid4())+'.'+filename.split('.')[-1])

# Create your models here.


class Categorie(models.Model):
    name= models.CharField(max_length=50,unique=True,default='')
    slug=models.SlugField(unique=True,max_length=50,default='')
    desc = models.CharField(max_length=50, default='')
    amazon_nodeid=models.CharField(max_length=50)
    amazon_index = models.CharField(max_length=50)
    image = StdImageField(upload_to=UploadToAutoSlug(populate_from='name'),variations={
        'thumbnail': {"width": 300, "height": 300, "crop": True}
    })
    is_top_display = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    #@models.permalink
    def get_absolute_url(self):
        return reverse('shopping:categories_detail',args=[self.amazon_index,self.amazon_nodeid,self.slug,1])

class Marque(models.Model):
    name = models.CharField(max_length=50,unique=True,default='')
    slug = models.CharField(max_length=50,unique=True)
    image = StdImageField(upload_to=UploadToAutoSlug(populate_from='name'), variations={
        'thumbnail': {"width": 80, "height": 80, "crop": True}
    })
    categories=models.ManyToManyField(Categorie)
    is_home_display = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('shopping:marques_detail', args=[self.slug])

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=60,help_text='Obligatoire : Insérer la référence et la marque pour un meilleur référencement')
    slug = models.SlugField(max_length=300,unique=True,help_text='Ce champ se construit automatiquement')
    uuid= models.UUIDField(auto_created=True,null=True)
    desc = models.TextField(help_text='Mettez une description unique et originale pour un meilleur référencement')
    amazon_asin = models.CharField(max_length=100,unique=True,help_text='Obligatoire')
    amazon_parent_asin= models.CharField(max_length=100,null=True,blank=True)
    amazon_isbn = models.CharField(max_length=100,null=True,blank=True)
    amazon_ean =models.CharField(max_length=100,null=True,blank=True)
    amazon_upc=models.CharField(max_length=100,null=True,blank=True)
    amazon_color = models.CharField(max_length=100,null=True,blank=True)
    amazon_sku = models.CharField(max_length=100,null=True,blank=True)
    amazon_mpn = models.CharField(max_length=100,null=True,blank=True)
    amazon_label =models.CharField(max_length=100,null=True,blank=True)
    amazon_title = models.CharField(max_length=300,help_text='Facultative')
    amazon_feature = models.TextField(help_text='Facultative',blank=True)
    amazon_price = models.CharField(default='',max_length=50)
    amazon_large_image_url =  models.CharField(default='',max_length=2000)
    amazon_medium_image_url = models.CharField(default='', max_length=2000,blank=True)
    amazon_small_image_url = models.CharField(default='', max_length=2000,blank=True)
    amazon_offer_url = models.CharField(default='', max_length=2000)
    amazon_index =models.CharField(max_length=50,null=False,default='')
    amazon_brand = models.CharField(max_length=50,null=True,blank=True)
    amazon_manufacturer=models.CharField(max_length=50,null=True,blank=True)
    amazon_editorial_reviews = models.TextField(blank=True,null=True)
    categorie= models.ForeignKey(Categorie,related_name='products')
    is_index = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


   # @models.permalink
    def get_absolute_url(self):
        if self.name:
            return reverse('shopping:products_details',args=[self.categorie.slug,self.slug])
        return reverse('shopping:nofollow_products_detail',args=[self.categorie.slug,self.amazon_asin,slugify(ascii(self.amazon_title))])

    class Meta:
        unique_together=('name','categorie')

class Word(models.Model):
    name = models.CharField(default='',unique=True,max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    desc = models.TextField(null=True,blank=True)
    categorie=models.ForeignKey(Categorie,related_name='words')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('name','categorie')
    def get_absolute_url(self):
        return  reverse('shopping:words_search',args=[self.categorie.slug,self.slug,1])