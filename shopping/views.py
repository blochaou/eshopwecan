from django.shortcuts import render ,get_object_or_404
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from amazon.api import AmazonAPI,AmazonSearch
from bottlenose import Amazon
from eshopwecan import settings
from .models import Categorie,Marque,Product,Word
import uuid
from itertools import islice
from haystack.query import SearchQuerySet,Raw

from haystack.utils.app_loading import haystack_get_model

# Create your views here.
amazon_api = AmazonAPI(settings.AMAZON_ACCESS_KEY, settings.AMAZON_SECRET_KEY, settings.AMAZON_ASSOC_TAG,region='FR')
amazon_api_bottlenose = Amazon(settings.AMAZON_ACCESS_KEY, settings.AMAZON_SECRET_KEY, settings.AMAZON_ASSOC_TAG)

def index(request):

    categories = Categorie.objects.filter(is_top_display=True)
    if not categories:
        categories = Categorie.objects.all()

    marques = Marque.objects.filter(is_home_display=True)[:12]
    if not marques:
        marques = Marque.objects.all()[:12]

    try:
        if settings.EWC_HOME_DEFAULT_KEYWORDS and settings.EWC_HOME_DEFAULT_CATEGORY:
            category = Categorie.objects.filter(slug=settings.EWC_HOME_DEFAULT_CATEGORY).first()
            ama_products = amazon_api.search_n(8,Keywords=settings.EWC_HOME_DEFAULT_KEYWORDS,SearchIndex=category.amazon_index)
            products = from_amazon_to_eshopwecan(ama_products, category)

    except:
        pass
    return render(request,'shopping/index.html',locals())

def toutes_categories(request):
    categories = Categorie.objects.all()
    return render(request,'shopping/all_categories.html',locals())

def categories_detail(request,ama_index,cat_id,slug,page):

    topCategorie = Categorie.objects.filter(amazon_index=ama_index).first()

    #Search categories in database
    categorie = Categorie.objects.filter(amazon_nodeid=cat_id).first()

    #Lookup node from Amazon
    browse_node = amazon_api.browse_node_lookup(BrowseNodeId=cat_id)

    #if categorie does not exists set from Amazon
    if not categorie:
        categorie = Categorie()
        categorie.name = browse_node[0].name
        categorie.amazon_nodeid = browse_node[0].id
        categorie.slug = slugify(categorie.name)
        categorie.amazon_index = ama_index



    #Loop from children
    categories = []
    try:
        if browse_node and browse_node[0].children:
            for node in browse_node[0].children:
                new_cat = Categorie()
                new_cat.name = node.name
                new_cat.amazon_nodeid = node.id
                new_cat.slug = slugify(new_cat.name)
                new_cat.amazon_index = ama_index
                categories.append(new_cat)
    except:
        pass

    try:

        current_page = 1 if not page else int(page)
        pages = [i for i in range(1, current_page + 2)]
        previous_page = current_page if current_page == 1 else current_page - 1
        ama_search = AmazonSearch(amazon_api.api, aws_associate_tag=settings.AMAZON_ASSOC_TAG, BrowseNode=categorie.amazon_nodeid,
                                  SearchIndex=ama_index)
        ama_search.current_page = current_page
        ama_products = list(islice(ama_search, 12))
        if len(ama_products) == 0:
            next_page = current_page
            pages = [i for i in range(1, current_page + 1)]
        elif current_page == 10:
            next_page = current_page
            pages = [i for i in range(1, current_page + 1)]
        else:
            next_page = current_page + 1
        pageurl = categorie.get_absolute_url()[:-1]
        products = from_amazon_to_eshopwecan(ama_products, topCategorie)
    except:
        pass




    return render(request, 'shopping/categories_detail.html', locals())

def buy_products(request,asin):
    amazon_asin = asin
    return render(request,'shopping/buy_products.html',locals())


def products_detail(request,cat_slug,slug):

    #Get product from index or database
    try:
        product = SearchQuerySet().models(Product).filter(slug__exact=slug,cat_slug=cat_slug)[0]
        categorie = Categorie()
        categorie.id = product.categorie[0]
        categorie.slug = product.categorie[1]
        categorie.name = product.categorie[2]
        categorie.amazon_nodeid = product.categorie[3]
        categorie.amazon_index = product.categorie[4]
        product.categorie = categorie
    except:
        product = get_object_or_404(Product, slug=slug, categorie__slug=cat_slug)
        categorie = product.categorie



    #Loads similars products
    try:
        search_words = [s for s in product.slug.split('-') if len(s)>3]
        for i in reversed(range(1,3)):
            word = ' '.join(search_words[:i])
            products =SearchQuerySet().exclude(slug=slug).filter(content=word)[:6]
            if products:
                break
    except:
        pass

    return render(request,'shopping/product_detail.html',locals())

def get_amazon_similar_products(request,index,asin):
    ama_products = amazon_api.similarity_lookup(ItemId=asin)
    categorie = get_object_or_404(Categorie,amazon_index=index)
    products = from_amazon_to_eshopwecan(ama_products,categorie)
    return render(request,'shared/amazon_similar.html',locals())

def get_amazon_node(request,index,nodeid):
    # Lookup node from Amazon
    browse_node = amazon_api.browse_node_lookup(BrowseNodeId=nodeid)

    # Loop from children
    categories = []
    try:
        if browse_node and browse_node[0].children:
            for node in browse_node[0].children:
                new_cat = Categorie()
                new_cat.name = node.name
                new_cat.amazon_nodeid = node.id
                new_cat.slug = slugify(new_cat.name)
                new_cat.amazon_index = index
                categories.append(new_cat)
    except:
        pass

    return render(request, 'shared/categorie_nodes.html', locals())


def nofollow_products_detail(request,cat_slug,asin,slug):
    categorie = Categorie.objects.filter(slug=cat_slug).first()

    amazon_product = amazon_api.lookup(ItemId=asin)
    ama_products = amazon_api.similarity_lookup(ItemId=asin)
    products= from_amazon_to_eshopwecan(ama_products,categorie)
    categories = []
    try:
        if amazon_product.browse_nodes:
            for node in amazon_product.browse_nodes:
                new_cat = Categorie()
                new_cat.name = node.name
                new_cat.amazon_nodeid = node.id
                new_cat.slug = slugify(new_cat.name)
                new_cat.amazon_index = categorie.amazon_index
                categories.append(new_cat)
    except:
        pass
    return render(request,'shopping/nofolowproduct.html',locals())
    pass

def get_product_price(request,asin):
    amazon_product = amazon_api.lookup(ItemId=asin)
    return render(request,'shared/product_price.html',locals())


def marques_detail(request,slug):

    pass


def words_search(request,cat_slug,word,page):
    categorie = get_object_or_404(Categorie,slug=cat_slug)
    word_search = get_object_or_404(Word,slug=word,categorie__id=categorie.id)
    try:
        browse_node = amazon_api.browse_node_lookup(BrowseNodeId=categorie.amazon_nodeid)
        current_page = 1 if not page else int(page)
        pages = [i for i in range(1, current_page + 2)]
        previous_page = current_page if current_page == 1 else current_page - 1
        ama_search = AmazonSearch(amazon_api.api, aws_associate_tag=settings.AMAZON_ASSOC_TAG, Keywords=word_search.name,
                                  SearchIndex=categorie.amazon_index)
        ama_search.current_page = current_page
        ama_products = list(islice(ama_search, 10))
        pageurl = word_search.get_absolute_url()[:-1]
        if len(ama_products) == 0:
            next_page = current_page
            pages = [i for i in range(1, current_page + 1)]
        elif current_page == 10:
            next_page = current_page
            pages = [i for i in range(1, current_page + 1)]
        else:
            next_page = current_page + 1

        products = from_amazon_to_eshopwecan(ama_products, categorie)

    except:
        pass


        # Loop from children
    categories = []
    try:
        if browse_node and browse_node[0].children:
            for node in browse_node[0].children:
                new_cat = Categorie()
                new_cat.name = node.name
                new_cat.amazon_nodeid = node.id
                new_cat.slug = slugify(new_cat.name)
                new_cat.amazon_index = categorie.amazon_index
                categories.append(new_cat)
    except:
        pass
    return render(request,'shopping/word_search.html',locals())


def search(request,page=1):
    amazon_index = request.GET['amazon_index']
    text_search = request.GET['text_search']
    try:
        current_page = int(request.GET['page'])
    except:
        current_page = page

    categorie = get_object_or_404(Categorie, amazon_index=amazon_index)


    try:
        browse_node = amazon_api.browse_node_lookup(BrowseNodeId=categorie.amazon_nodeid)
        pages = [i for i in range(1, current_page + 2)]
        previous_page = current_page if current_page == 1 else current_page - 1
        ama_search = AmazonSearch(amazon_api.api,aws_associate_tag=settings.AMAZON_ASSOC_TAG,Keywords=text_search,SearchIndex=amazon_index)
        ama_search.current_page = current_page
        ama_products = list(islice(ama_search,10))
        pageurl = "/search?amazon_index="+amazon_index+"&text_search="+text_search+"&page="
        if len(ama_products) == 0:
            next_page = current_page
            pages = [i for i in range(1, current_page + 1)]
        elif current_page==10:
            next_page=current_page
            pages = [i for i in range(1, current_page + 1)]
        else:
            next_page =  current_page+1

        products = from_amazon_to_eshopwecan(ama_products, categorie)

    except:
        pass

    categories = []
    try:
        if browse_node and browse_node[0].children:
            for node in browse_node[0].children:
                new_cat = Categorie()
                new_cat.name = node.name
                new_cat.amazon_nodeid = node.id
                new_cat.slug = slugify(new_cat.name)
                new_cat.amazon_index = categorie.amazon_index
                categories.append(new_cat)
    except:
        pass

    return render(request,'shopping/search_result.html',locals())

@csrf_exempt
def add_to_db(request):
    try:
        saving_product = Product()
        saving_product.name =request.POST['product_title_form']
        saving_product.slug = slugify(saving_product.name)
        saving_product.uuid = uuid.uuid4()
        saving_product.desc = request.POST['product_desc_form']
        saving_product.amazon_asin=request.POST['product_asin_form']
        saving_product.amazon_parent_asin = request.POST['product_parent_asin_form']
        saving_product.amazon_isbn = request.POST['product_isbn_form']
        saving_product.amazon_ean = request.POST['product_ean_form']
        saving_product.amazon_upc = request.POST['product_upc_form']
        saving_product.amazon_color = request.POST['product_color_form']
        saving_product.amazon_sku = request.POST['product_sku_form']
        saving_product.amazon_mpn = request.POST['product_mpn_form']
        saving_product.amazon_label = request.POST['product_label_form']
        saving_product.amazon_title = request.POST['product_ama_title_form']
        saving_product.amazon_feature = request.POST['product_features_form']
        saving_product.amazon_price = request.POST['product_price_form']
        saving_product.amazon_large_image_url = request.POST['product_image_large_form']
        saving_product.amazon_medium_image_url = request.POST['product_image_medium_form']
        saving_product.amazon_small_image_url = request.POST['product_image_small_form']
        saving_product.amazon_offer_url = 'https://www.amazon.fr/dp/{0}/?tag={1}'.format(saving_product.amazon_asin,settings.AMAZON_ASSOC_TAG)
        saving_product.amazon_index = request.POST['product_index_form']
        saving_product.amazon_brand = request.POST['product_brand_form']
        saving_product.amazon_manufacturer = request.POST['product_manufacturer_form']
        saving_product.amazon_editorial_reviews = request.POST['product_editorial_reviews_form']
        saving_product.categorie_id = int(request.POST['product_categorie_id_form'])

        saving_product.full_clean()
        saving_product.save()
    except ValidationError as err:
         return JsonResponse({'result': False, 'error': ';'.join(err.messages)})

    except Exception as err :
        return JsonResponse({'result': False, 'error': err.args})

    return JsonResponse({'result': True, 'error':'Impossible '})



def from_amazon_to_eshopwecan(ama_products,topCat):
    ewc_products = []

    for p in ama_products:
        new_product = Product.objects.filter(amazon_asin=p.asin).first()
        if not new_product:
            new_product = Product()
            new_product.categorie = topCat
            new_product.amazon_index = topCat.amazon_index

        new_product.amazon_asin =  p.asin
        new_product.amazon_title = p.title
        new_product.amazon_brand ='' if p.brand is None else p.brand
        new_product.amazon_color = '' if p.color is None else p.color
        new_product.amazon_isbn = '' if p.isbn is None else p.isbn
        new_product.amazon_ean ='' if p.ean is None else p.ean
        new_product.amazon_label = '' if p.label is None else p.label
        new_product.amazon_manufacturer ='' if p.manufacturer is None else p.manufacturer
        new_product.amazon_mpn ='' if p.mpn is None else p.mpn
        new_product.amazon_parent_asin ='' if p.parent_asin is None else p.parent_asin
        new_product.amazon_sku ='' if p.sku is None else p.sku
        new_product.amazon_upc = '' if p.upc is None else p.upc
        new_product.amazon_editorial_reviews ='.'.join(p.editorial_reviews)
        new_product.amazon_feature = ', '.join(p.features)
        new_product.amazon_price ='' if p.price_and_currency is None else  p.price_and_currency
        new_product.amazon_large_image_url ='' if p.large_image_url is None else p.large_image_url
        new_product.amazon_medium_image_url ='' if p.medium_image_url is None else p.medium_image_url
        new_product.amazon_small_image_url ='' if p.small_image_url is None else p.small_image_url
        new_product.amazon_offer_url ='' if p.offer_url is None else p.offer_url


        ewc_products.append(new_product)

    return  ewc_products

def handle_404(request):
    response = render(request,'shopping/404.html',locals())
    response.status_code = 400
    return response

def handle_500(request):
    response = render(request,'shopping/500.html',locals())
    response.status_code = 500
    return response