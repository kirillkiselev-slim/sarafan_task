import json
from http import HTTPStatus

from django.test import TestCase, Client
from django.contrib.auth import get_user_model, get_user
from django.urls import reverse

from product.models import ShoppingCart, Product
from category.models import Subcategory, Category
from .constants import (CATEGORY_TESTS, SUBCATEGORY_TESTS, POST_SHOPPING_CART,
                        START_TEST_SUBCATEGORY, END_TEST_SUBCATEGORY,
                        PUT_SHOPPING_CART, USER_CREDS)

User = get_user_model()


class TestSarafanBaseCase(TestCase):
    """
    Базовый класс для тестов, содержит общие данные для
    категорий и подкатегорий.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Метод для установки тестовых данных категорий и подкатегорий.
        Создает категорию и несколько подкатегорий для тестов.
        """
        cls.category = Category.objects.create(**CATEGORY_TESTS)

        cls.subcategories = [Subcategory.objects.create(
            title=f'{SUBCATEGORY_TESTS.get('title')}{i}',
            slug=f'{SUBCATEGORY_TESTS.get('slug')}{i}',
            category=cls.category
        ) for i in range(START_TEST_SUBCATEGORY, END_TEST_SUBCATEGORY)]


class TestCategory(TestSarafanBaseCase):

    def test_subcategories_availability_under_category(self):
        """
        Тест проверки наличия подкатегорий под категорией.
        Получает список категорий через API и сравнивает их с
        созданными подкатегориями.
        """
        url = reverse('api:categories-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK, 'Не 200 статус')
        subcategories = response.json()[0].get('subcategories', None)
        self.assertIsNotNone(subcategories, 'Подкатегория отсутствует')
        created_subcategories = [name.title for name in self.subcategories]
        self.assertListEqual(list1=created_subcategories, list2=subcategories)


class TestShoppingCart(TestSarafanBaseCase):
    """
    Класс тестирования корзины покупок.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Метод установки тестовых данных для корзины покупок.
        Создает продукт, пользователя и подготавливает данные для запросов.
        """
        super().setUpTestData()
        url_token = reverse('api:jwt-create')

        cls.subcategory = Subcategory.objects.create(
            title=f'subcategory-test-shopping-cart',
            slug=f'subcategory-test-shopping-cart',
            category=cls.category
        )
        cls.product = Product.objects.create(
            name='iPhone 13',
            price=799.99,
            category=cls.category,
            subcategory=cls.subcategory,
            slug='iphone-13'
        )
        cls.user = User.objects.create(**USER_CREDS)
        cls.user.set_password('random-pass!!')
        cls.user.save()

        cls.product_url = reverse('api:shopping-cart',
                                  kwargs={'product_pk': cls.product.pk})

        cls.user_client = Client()
        cls.user_client.force_login(cls.user)

        data = {'username': cls.user.username, 'password': 'random-pass!!'}
        response = cls.user_client.post(url_token, data=data)
        token = response.data['access']
        cls.headers = {'Authorization': f'Bearer {token}'}

        cls.post_shopping_cart_response = cls.user_client.post(
            cls.product_url, headers=cls.headers, data=POST_SHOPPING_CART)

    def test_add_product(self):
        """
        Тест добавления продукта в корзину покупок.
        Проверяет успешность добавления продукта в корзину.
        """
        self.assertEqual(
            self.post_shopping_cart_response.status_code, HTTPStatus.CREATED,
            'Не 201 статус')
        shopping_cart = ShoppingCart.objects.count()
        self.assertEqual(shopping_cart, 1)
        user = get_user(self.user_client)
        self.assertEqual(user, self.user)
        shopping_cart = json.loads(
            self.post_shopping_cart_response.content)
        self.assertEqual(self.user.username, shopping_cart.get('user'))

    def test_change_amount_product(self):
        """
        Тест изменения количества продукта в корзине.
        Проверяет успешность изменения количества продукта.
        """
        amount_before = ShoppingCart.objects.first().amount
        response = self.user_client.put(
            self.product_url,
            headers=self.headers,
            content_type='application/json',
            data=PUT_SHOPPING_CART)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        amount_after = response.json().get('amount', None)
        self.assertIsNotNone(amount_after, 'Кол-во отсутствует')
        self.assertNotEqual(amount_before, amount_after)
