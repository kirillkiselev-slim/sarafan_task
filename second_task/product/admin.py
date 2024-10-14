from django.contrib import admin

from product.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'subcategory', 'category')
    list_select_related = ('subcategory', 'category')
    list_editable = ('subcategory', 'category')
    list_filter = ('slug', 'subcategory', 'category')
    search_fields = ('name', 'slug')


admin.site.register(Product, ProductAdmin)