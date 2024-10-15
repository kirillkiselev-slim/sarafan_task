from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import (ProductViewSet, CategoryViewSet, ShoppingCartGeneric,
                    SubcategoryViewSet, ShoppingCartViewSet, ClearShoppingCart)


app_name = 'api'


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'subcategories', SubcategoryViewSet,
                basename='subcategories')
router.register(r'my-shopping-cart', ShoppingCartViewSet,
                basename='shopping-cart-info')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('shopping-cart/<int:product_pk>', ShoppingCartGeneric.as_view(),
         name='shopping-cart'),
    path('shopping-cart/clear/', ClearShoppingCart.as_view(),
         name='clear-shopping-cart'),
]

schema_view = get_schema_view(
    openapi.Info(
        title='Store API',
        default_version='v1',
        description='Документация для приложения Store проекта Sarafan',
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny], validators=['ssv']
)

urlpatterns += [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui')
]