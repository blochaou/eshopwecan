from django.contrib import admin
from .models import Categorie,Marque,Product,Word
# Register your models here.

class MarqueAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image','is_home_display','date_creation','date_update',)
    list_filter = ('name', )
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'date_creation'
    ordering = ['name', 'date_update']

class CategorieAdmin(admin.ModelAdmin):
    list_display = ('name','slug','amazon_index','image','is_top_display')
    list_filter = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'date_creation'
    ordering = ['name', 'date_update']

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','slug','amazon_asin','is_index')
    list_filter = ('name','amazon_asin')
    search_fields = ('name','reference','amazon_asin')
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'date_creation'
    ordering = ['name', 'date_update']

class WordAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'categorie')
    list_filter = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'date_creation'
    ordering = ['name']


admin.site.register(Marque, MarqueAdmin)
admin.site.register(Categorie,CategorieAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Word,WordAdmin)