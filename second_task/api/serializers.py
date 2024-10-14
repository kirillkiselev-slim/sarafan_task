import base64

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError

from product.models import Product, ShoppingCart
from category.models import Category, Subcategory
from rest_framework.validators import UniqueTogetherValidator

from .constants import ALREADY_IN_SHOPPING_CART, NOT_IN_SHOPPING_CART


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, image_data):
        if isinstance(image_data, str) and image_data.startswith('data:image'):
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr),
                                     name=f'temp.{ext}')

        return super().to_internal_value(image_data)


class SarafanBaseSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True, allow_null=False)

    class Meta:
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    thumbnail = Base64ImageField(required=True, allow_null=False)
    large = Base64ImageField(required=True, allow_null=False)
    medium = Base64ImageField(required=True, allow_null=False)
    category = serializers.StringRelatedField(read_only=True)
    subcategory = serializers.StringRelatedField(read_only=True)

    class Meta(SarafanBaseSerializer.Meta):
        model = Product

    def to_representation(self, instance):
        data = super().to_representation(instance)
        thumbnail, medium, large = (data.pop('thumbnail'),
                                    data.pop('medium'),
                                    data.pop('large'))
        list_images = [
            {'thumbnail': thumbnail, 'medium': medium, 'large': large}
        ]
        data['images'] = list_images
        return data


class CategorySerializer(SarafanBaseSerializer):
    class Meta(SarafanBaseSerializer.Meta):
        model = Category

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['subcategories'] = [obj.title for obj in instance.subcategory.all()]
        return data


class SubcategorySerializer(SarafanBaseSerializer):
    category = serializers.StringRelatedField(read_only=True)

    class Meta(SarafanBaseSerializer.Meta):
        model = Subcategory


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = ShoppingCart
        fields = '__all__'
        read_only_fields = ('product', 'is_in_shopping_cart')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'product')
            )
        ]

    def get_request(self):
        return self.context.get('request')

    def get_user(self):
        return self.get_request().user

    def get_product(self):
        pk = self.get_request().parser_context.get('kwargs').get('pk')
        return get_object_or_404(Product, pk=pk)

    def validate(self, shopping_cart_data):
        product = self.get_product()
        request = self.get_request()
        user = self.get_user()
        query = ShoppingCart.objects.filter(
            product=product, user=user,
            is_in_shopping_cart=True).exists()
        if request.method in 'POST':
            if query:
                raise ValidationError(ALREADY_IN_SHOPPING_CART)

        if request.method == 'DELETE':
            if not query:
                raise ValidationError(NOT_IN_SHOPPING_CART)
        return shopping_cart_data

    def update_or_create_shopping_cart(self, user, product, amount):
        cart, _ = ShoppingCart.objects.update_or_create(
            product=product, user=user,
            defaults={'is_in_shopping_cart': True},
            amount=amount)
        return cart

    def create(self, validated_data):
        self.update_or_create_shopping_cart(
            product=self.get_product(), user=self.get_user(),
            amount=validated_data.get('amount'))

    def update(self, instance, validated_data):
        self.update_or_create_shopping_cart(
            product=self.get_product(), user=self.get_user(),
            amount=validated_data.get('amount'))
