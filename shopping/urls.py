from django.conf.urls import url
from . import views
from django.contrib.sitemaps.views import sitemap
from shopping.sitemaps import ProductSitemap,WordSitemap

sitemaps = {
       'products': ProductSitemap,
       'words':WordSitemap,
}



urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^toutes-les-categories/$',views.toutes_categories,name='toute-les-categories'),
    url(r'^categories/(?P<ama_index>[\w]+)/(?P<cat_id>[\d]+)/(?P<slug>[-\w]+)/(?P<page>[\d]*)$', views.categories_detail, name='categories_detail'),
    url(r'^marques/(?P<slug>[-\w]+)$', views.marques_detail, name='marques_detail'),
    url(r'^buy-products/(?P<asin>[\d\w]+)$', views.buy_products, name='buy_products'),
    url(r'^product-price/(?P<asin>[\d\w]+)$', views.get_product_price, name='products_price'),
    url(r'^product/(?P<cat_slug>[-\w]+)/(?P<slug>[-\w]+)$',views.products_detail,name='products_details'),
    url(r'^rechercher/(?P<cat_slug>[-\w]+)/(?P<word>[-\w]+)/(?P<page>[\d]*)$', views.words_search,name='words_search'),
    url(r'^nofolowproduct/(?P<cat_slug>[-\w]+)/(?P<asin>[\d\w]+)/(?P<slug>[-\w]+)$',views.nofollow_products_detail,name='nofollow_products_detail'),
    url(r'^search',views.search,name='user_search'),
    url(r'^add_to_db',views.add_to_db,name='add_to_db'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),
    url(r'^loadnode/(?P<index>[\w]+)/(?P<nodeid>[\d]+)$',views.get_amazon_node,name='load_amazon_nodes_children'),
    url(r'^loadsimilar/(?P<index>[\w]+)/(?P<asin>[\d\w]+)$',views.get_amazon_similar_products,name='amazon_similar_products')

]

