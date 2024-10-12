from rest_framework import serializers

from product.models import Product
from category.models import Category, Subcategory


class SarafanBaseSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Subcategory
        fields = '__all__'

