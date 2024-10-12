from django.contrib import admin

from category.models import Category, Subcategory
from product.models import Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    search_fields = ('slug', 'title')
    list_filter = ('slug',)
    list_display_links = ('slug', 'title')


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category',)
    list_select_related = ('category',)
    list_editable = ('category',)
    search_fields = ('slug', 'title')
    list_filter = ('slug',)
    list_display_links = ('slug', 'title')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'subcategory', 'category')
    list_select_related = ('subcategory', 'category')
    list_editable = ('subcategory', 'category')
    list_filter = ('slug', 'subcategory', 'category')
    search_fields = ('name', 'slug')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
