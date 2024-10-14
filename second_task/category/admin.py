from django.contrib import admin

from category.models import Category, Subcategory


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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubCategoryAdmin)

