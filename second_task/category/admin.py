from django.contrib import admin

from category.models import Category, Subcategory
from product.models import Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    search_fields = ('slug', 'title')
    list_filter = ('slug',)
    list_display_links = ('slug',)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category',)
    list_select_related = ('category',)
    list_editable = ('category',)
    search_fields = ('slug', 'title')
    list_filter = ('slug',)
    list_display_links = ('slug',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)
    list_select_related = ('subcategory',)
    list_editable = ('subcategory',)
    search_fields = ('name',)
    list_filter = ('subcategory',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
