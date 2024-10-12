from django.db import models

from core.models import BaseModel


class Category(BaseModel):
    title = models.CharField(max_length=64, verbose_name='Категория')

    image = models.ImageField(upload_to='categories/',
                              verbose_name='Фото категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Subcategory(BaseModel):
    title = models.CharField(max_length=64, verbose_name='Подкатегории')

    image = models.ImageField(upload_to='subcategories/',
                              verbose_name='Фото подкатегории')
    category = models.ForeignKey(
        Category, verbose_name='Категории', related_name='subcategory',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.title