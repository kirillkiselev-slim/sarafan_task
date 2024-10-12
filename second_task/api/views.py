from django.contrib.auth import get_user_model
from rest_framework import viewsets, status

from product.models import Product
from category.models import Category, Subcategory
from .permissions import ReadOrAdminOnly
from .pagination import SarafanPageNumberPagination

User = get_user_model()


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = ReadOrAdminOnly
    # serializer_class = ...
    pagination_class = SarafanPageNumberPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = ReadOrAdminOnly
    pagination_class = SarafanPageNumberPagination

