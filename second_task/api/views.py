from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce

from rest_framework.response import Response
from product.models import Product, ShoppingCart
from category.models import Category, Subcategory
from rest_framework.decorators import action
from .permissions import ReadOrAdminOnly, AuthorOrAdminOnly
from .pagination import SarafanPageNumberPagination
from .serializers import (ProductSerializer, CategorySerializer,
                          ShoppingCartPostPutDeleteSerializer,
                          SubcategorySerializer, ShoppingCartGetSerializer)

User = get_user_model()


class SarafanViewSet(viewsets.ModelViewSet):
    pagination_class = SarafanPageNumberPagination
    permission_classes = (ReadOrAdminOnly,)
    http_method_names = ('get',)


class ProductViewSet(SarafanViewSet):
    queryset = Product.objects.all()

    # serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.action in {'retrieve', 'list'}:
            return ProductSerializer
        return ShoppingCartPostPutDeleteSerializer

    def get_permissions(self):
        if self.action in {'retrieve', 'list'}:
            self.permission_classes = (ReadOrAdminOnly,)
        else:
            self.permission_classes = (AuthorOrAdminOnly,)
        return super().get_permissions()

    def get_user(self):
        return self.request.user

    def get_shopping_cart(self):
        return get_object_or_404(ShoppingCart, user=self.get_user(),
                                 product=self.get_object())

    def shopping_cart_serializer(self):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return serializer

    @action(methods=('post',), detail=True, url_path='add-to-shopping-cart')
    def add_to_cart(self, request, *args, **kwargs):
        self.shopping_cart_serializer()
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=('put',), detail=True,
            url_path='update-in-shopping-cart-')
    def update_cart(self, request, *args, **kwargs):
        self.shopping_cart_serializer()
        return Response(status=status.HTTP_200_OK)

    @action(methods=('delete',), detail=True,
            url_path='delete-in-shopping-cart')
    def delete_shopping_cart(self, request, *args, **kwargs):
        shopping_cart = self.get_shopping_cart()
        shopping_cart.is_in_shopping_cart = False
        shopping_cart.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # @action('get', detail=False, url_path='shopping-cart-information')

    @action(methods=('delete',), detail=False,
            url_path='clear-shopping-cart')
    def clear_shopping_cart(self, request, *args, **kwargs):
        user = self.get_user()
        (ShoppingCart.objects.filter(
            user=user, is_in_shopping_cart=True)
         .update(is_in_shopping_cart=False, amount=0))

        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(SarafanViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryViewSet(SarafanViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class ShoppingCartViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingCartGetSerializer
    permission_classes = (AuthorOrAdminOnly,)

    @action(methods=('get',), detail=False, url_path='shopping-cart-information')
    def get_shopping_cart(self, request, *args, **kwargs):
        user = self.request.user
        queryset = ShoppingCart.objects.filter(
            user=user, is_in_shopping_cart=True
        ).annotate(
            product_name=F('product__name'), product_price=F('product__price'),
            total_price=F('amount') * F('product__price')
        ).values('product_name', 'amount',
                 'product_price', 'total_price')
        cart_summary = queryset.aggregate(
            total_items=Sum('amount'),
            total_cart_price=Coalesce(Sum(F('amount') * F('product__price')),
                                      Value(0))
        )
        return Response({
            'cart_contents': list(queryset),
            'total_items': cart_summary['total_items'],
            'total_price': cart_summary['total_cart_price'],
        })
