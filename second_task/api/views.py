from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, generics
from django.db.models import Sum, F, Value, ExpressionWrapper, DecimalField
from django.db.models.functions import Coalesce

from rest_framework.response import Response
from product.models import Product, ShoppingCart
from category.models import Category, Subcategory
from rest_framework.decorators import action
from .permissions import ReadOrAdminOnly, AuthorOnly
from .pagination import SarafanPageNumberPagination
from .serializers import (ProductSerializer, CategorySerializer,
                          ShoppingCartPostPutDeleteSerializer,
                          SubcategorySerializer)
from .constants import SUCCESS_MESSAGE

User = get_user_model()


class SarafanViewSet(viewsets.ModelViewSet):
    """
    Базовый ViewSet для API Sarafan, задающий общие настройки пагинации,
    прав доступа и допустимые HTTP-методы.
    """

    pagination_class = SarafanPageNumberPagination
    permission_classes = (ReadOrAdminOnly,)
    http_method_names = ('get',)


class CategoryViewSet(SarafanViewSet):
    """
    ViewSet для управления объектами Category, использующий базовые
    настройки SarafanViewSet.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryViewSet(SarafanViewSet):
    """
    ViewSet для управления объектами Subcategory, унаследованный от
    SarafanViewSet с использованием SubcategorySerializer.
    """
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class ProductViewSet(SarafanViewSet):
    """
    ViewSet для управления объектами Product, использующий базовые
    права доступа и ProductSerializer.
    """

    queryset = Product.objects.all()
    permission_classes = (ReadOrAdminOnly,)
    serializer_class = ProductSerializer


class ShoppingCartViewSet(viewsets.ViewSet):
    """
    ViewSet для просмотра корзины покупок пользователя. Включает действие
    для получения содержимого корзины и общего количества товаров.
    """

    permission_classes = (AuthorOnly,)

    @action(methods=('get',), detail=False, url_path='view-my-cart')
    def get_shopping_cart(self, request, *args, **kwargs):
        user = self.request.user
        queryset = ShoppingCart.objects.filter(
            user=user, is_in_shopping_cart=True
        ).annotate(
            product_name=F('product__name'),
            product_price=F('product__price'),
            total_price=ExpressionWrapper(
                F('amount') * F('product__price'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        ).values('product_name', 'amount', 'product_price', 'total_price')

        cart_summary = queryset.aggregate(
            total_items=Sum('amount'),
            total_cart_price=Coalesce(
                ExpressionWrapper(
                    Sum(F('amount') * F('product__price')),
                    output_field=DecimalField(max_digits=10, decimal_places=2)
                ),
                Value(0, output_field=DecimalField(
                    max_digits=10, decimal_places=2))
            )
        )

        return Response({
            'cart_contents': list(queryset),
            'total_items': cart_summary['total_items'],
            'total_price': cart_summary['total_cart_price'],
        })


class ShoppingCartGeneric(generics.GenericAPIView):
    """
    GenericAPIView для управления объектами ShoppingCart с действиями
    для создания, обновления и удаления корзины покупок.
    """

    queryset = ShoppingCart.objects.all()
    permission_classes = (AuthorOnly,)
    lookup_field = 'product'
    lookup_url_kwarg = 'product_pk'
    serializer_class = ShoppingCartPostPutDeleteSerializer

    def get_user(self):
        return self.request.user

    def shopping_cart_serializer(self):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return serializer

    def post(self, request, *args, **kwargs):
        serializer = self.shopping_cart_serializer()
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    def put(self, request, *args, **kwargs):
        serializer = self.shopping_cart_serializer()
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def delete(self, request, *args, **kwargs):
        shopping_cart = self.get_object()
        shopping_cart.is_in_shopping_cart = False
        shopping_cart.save()
        return Response(
            status=status.HTTP_204_NO_CONTENT, data=SUCCESS_MESSAGE)


class ClearShoppingCart(generics.GenericAPIView):
    """
    GenericAPIView для очистки корзины пользователя.
    """

    permission_classes = (AuthorOnly,)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        (ShoppingCart.objects.filter(
            user=user, is_in_shopping_cart=True)
         .update(is_in_shopping_cart=False, amount=0))

        return Response(
            status=status.HTTP_204_NO_CONTENT, data=SUCCESS_MESSAGE)
