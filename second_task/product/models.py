from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from versatileimagefield.fields import VersatileImageField

from core.models import BaseModel


User = get_user_model()


class Product(BaseModel):
    name = models.CharField(max_length=64, verbose_name='товар')

    image = VersatileImageField(upload_to='products/',
                                verbose_name='Фото категории')
    price = models.PositiveIntegerField(
        verbose_name='Цена', validators=(
            MinValueValidator(1,
                              message='Цена должна'' быть больше или равно 1'), ))

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
        verbose_name='Подкатегория')

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
