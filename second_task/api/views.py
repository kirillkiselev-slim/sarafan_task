from django.contrib.auth import get_user_model
from rest_framework import viewsets, status

from product.models import Product, ShoppingCart
from category.models import Category, Subcategory
from rest_framework.decorators import action, api_view
from .permissions import ReadOrAdminOnly, AuthorOrAdminOnly
from .pagination import SarafanPageNumberPagination
from .serializers import (ProductSerializer, CategorySerializer,
                          SubcategorySerializer, ShoppingCartSerializer)

User = get_user_model()


class SarafanViewSet(viewsets.ModelViewSet):
    pagination_class = SarafanPageNumberPagination
    permission_classes = (ReadOrAdminOnly,)


class ProductViewSet(SarafanViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(SarafanViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryViewSet(SarafanViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class ShoppingCartViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingCartSerializer
    permission_classes = (AuthorOrAdminOnly,)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
