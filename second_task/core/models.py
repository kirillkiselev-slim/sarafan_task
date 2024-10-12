from django.db import models
from django.core.validators import validate_slug


class BaseModel(models.Model):
    """Абстрактный класс."""

    slug = models.SlugField(max_length=64, unique=True, verbose_name='Слаг',
                            validators=(validate_slug,), default=None)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        abstract = True

    def __repr__(self):
        return self.slug
