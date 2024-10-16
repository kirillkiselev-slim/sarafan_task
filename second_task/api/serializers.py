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
    """
    Кастомное поле для обработки изображений, закодированных в формате
    Base64. Преобразует строку Base64 в объект ContentFile, который
    можно сохранить как изображение.
    """

    def to_internal_value(self, image_data):
        if isinstance(image_data, str) and image_data.startswith('data:image'):
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr),
                                     name=f'temp.{ext}')

        return super().to_internal_value(image_data)


class SarafanBaseSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для моделей с поддержкой Base64 изображений.
    """

    image = Base64ImageField(required=True, allow_null=False)

    class Meta:
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product, который обрабатывает изображения
    (thumbnail, medium, large) в формате Base64 и выводит категории и
    подкатегории как строки.
    """

    thumbnail = Base64ImageField(required=True, allow_null=False)
    large = Base64ImageField(required=True, allow_null=False)
    medium = Base64ImageField(required=True, allow_null=False)
    category = serializers.StringRelatedField(read_only=True)
    subcategory = serializers.StringRelatedField(read_only=True)

    class Meta(SarafanBaseSerializer.Meta):
        model = Product

    def to_representation(self, instance):
        """
        Возвращает представление данных продукта с изображениями,
        сгруппированными в список.
        """
        data = super().to_representation(instance)
        thumbnail, medium, large = (data.pop('thumbnail'), data.pop('medium'),
                                    data.pop('large'))
        list_images = [
            {'thumbnail': thumbnail, 'medium': medium, 'large': large}
        ]
        data['images'] = list_images
        return data


class CategorySerializer(SarafanBaseSerializer):
    """
    Сериализатор для модели Category. Добавляет список подкатегорий
    по названию в представление данных.
    """

    class Meta(SarafanBaseSerializer.Meta):
        model = Category

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['subcategories'] = [obj.title for obj in
                                 instance.subcategory.all()]
        return data


class SubcategorySerializer(SarafanBaseSerializer):
    """
    Сериализатор для модели Subcategory. Выводит категорию как имя.
    """

    category = serializers.StringRelatedField(read_only=True)

    class Meta(SarafanBaseSerializer.Meta):
        model = Subcategory


class BaseShoppingCartSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для объектов ShoppingCart.
    """

    class Meta:
        model = ShoppingCart

    def get_request(self):
        return self.context.get('request')

    def get_user(self):
        request = self.get_request()
        return request.user


class ShoppingCartPostPutDeleteSerializer(BaseShoppingCartSerializer):
    """
    Сериализатор для создания, обновления и удаления объектов
    ShoppingCart.
    """

    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta(BaseShoppingCartSerializer.Meta):
        fields = ('amount', 'user')
        read_only_fields = ('is_in_shopping_cart', 'product')

    def get_product(self):
        product = self.get_request().parser_context.get(
            'kwargs').get('product_pk')
        return get_object_or_404(Product, pk=product)

    def validate(self, shopping_cart_data):
        """
        Проверяет наличие продукта в корзине. Если продукт уже в
        корзине при POST-запросе, возвращает ошибку. Если продукта
        нет в корзине при PUT-запросе, также возвращает ошибку.
        """
        request = self.get_request()
        product = self.get_product()
        shopping_cart_data['product'] = product
        user = self.get_user()
        query = ShoppingCart.objects.filter(
            product=product, user=user,
            is_in_shopping_cart=True).exists()
        if request.method in 'POST':
            if query:
                raise ValidationError(ALREADY_IN_SHOPPING_CART)

        elif request.method == 'PUT':
            if not query:
                raise ValidationError(NOT_IN_SHOPPING_CART)
        return shopping_cart_data

    def update_or_create_shopping_cart(self, user, product, amount):
        """
        Обновляет или создает объект корзины покупок для текущего
        пользователя и продукта.
        """
        cart, _ = ShoppingCart.objects.update_or_create(
            product=product, user=user,
            defaults={'is_in_shopping_cart': True, 'amount': amount})
        return cart

    def create(self, validated_data):
        cart = self.update_or_create_shopping_cart(
            product=self.get_product(), user=self.get_user(),
            amount=validated_data.get('amount'))
        return cart

    def update(self, instance, validated_data):
        cart = self.update_or_create_shopping_cart(
            product=self.get_product(), user=self.get_user(),
            amount=validated_data.get('amount'))
        return cart

    def to_representation(self, instance):
        """
        Возвращает представление данных объекта корзины покупок,
        добавляя имя пользователя и название продукта.
        """
        data = super().to_representation(instance)
        data['id'] = instance.id
        data['user'] = instance.user.username
        data['product'] = instance.product.name
        return data
