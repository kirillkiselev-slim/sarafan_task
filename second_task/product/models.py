from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from versatileimagefield.fields import VersatileImageField

from core.models import BaseModel
from category.models import Category, Subcategory

User = get_user_model()


class Product(BaseModel):
    name = models.CharField(max_length=64, verbose_name='товар')

    price = models.DecimalField(
        verbose_name='Цена', decimal_places=2, validators=(
            MinValueValidator(
                1,
                message='Цена должна'' быть больше или равно 1'),),
        max_digits=10,)
    category = models.ForeignKey(
        Category, verbose_name='Категория', related_name='products',
        on_delete=models.PROTECT)
    subcategory = models.ForeignKey(
        Subcategory, verbose_name='Подкатегория',
        related_name='%(class)s_products', on_delete=models.PROTECT)

    thumbnail = VersatileImageField(upload_to='images/products/thumbnails/',
                                    verbose_name='Миниатюра')
    medium = VersatileImageField(upload_to='images/products/medium/',
                                 verbose_name='Среднее изображение')
    large = VersatileImageField(upload_to='images/products/large/',
                                verbose_name='Большое изображение')

    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товар'

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    is_in_shopping_cart = models.BooleanField(
        default=False, verbose_name='в корзине')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Продукт')
    amount = models.PositiveIntegerField(verbose_name='Кол-Во', validators=(
        MinValueValidator(
            1,
            message='Кол-во должна'' быть больше или равно 1'),))

    class Meta:
        ordering = ('user',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'product'), name='user_product')
        ]

    def __str__(self):
        return f'Корзина {self.user} с продуктом "{self.product}"'
