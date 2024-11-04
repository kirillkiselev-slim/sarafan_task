# Описание

#### Этот проект представляет собой интернет-магазин, в котором пользователи могут просматривать товары, категории, подкатегории и добавлять товары в корзину. Основные функциональные возможности включают:

1. Категории и подкатегории товаров: Каждый товар привязан к определенной категории и подкатегории, что помогает пользователям легко находить интересующие их продукты.

2. Продукты: Товары содержат информацию о названии, цене и изображениях (миниатюра, среднее и большое изображения), что позволяет пользователям видеть детальные описания продуктов.

3. Корзина покупок: Пользователи могут добавлять товары в свою корзину, изменять их количество и удалять товары из корзины. Для каждого пользователя создается уникальная корзина, связанная с их аккаунтом.

4. Авторизация и аутентификация: Для использования функционала корзины и оформления заказов пользователи должны войти в систему через систему JWT-аутентификации.

5. Тестирование: В проекте реализованы тесты для проверки работы API, которые включают добавление товаров в корзину, изменение количества товаров и тд.


## **Запустить проект локально**

## Установка

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:kirillkiselev-slim/sarafan_task.git
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv env
```

* Если у вас Linux/macOS

    ```bash
    source env/bin/activate
    ```

* Если у вас windows

    ```commandline
    source env/scripts/activate
    ```

```bash
python3 -m pip install --upgrade pip
```
Создать свой .env файл и положите туда ваш DJANGO_KEY. Используйте этот [генератор](https://djecrety.ir/), например:

Для Linux/Mac
```bash
touch second_task/.env
```

Для Windows
```commandline
type nul > .\second_task\.env
```
Перейдите в .env файл и положите туда ключ, пример ниже.

```text
DJANGO_KEY=<your-random-key>
```

Установить зависимости из файла requirements.txt:

```bash
cd second_task
```

```bash
pip install -r requirements.txt
```
```bash
python manage.py migrate && python manage.py makemigrations
```
Еще раз сделайте миграции
```bash
python manage.py migrate
```

## Загрузите фикстуры

```bash
python manage.py loaddata fixtures/initial_data.json 
```

## Прoйдитесь тестами и убедитесь, что они проходят

```bash
python manage.py test api
```

#### Result example:

```text 
Ran 3 tests in 0.585s

OK
```

## Примеры запросов локально

Swagger документация: `http://127.0.0.1:8000/api/swagger/`

***Вам нужно будет получить токен с `http://127.0.0.1:8000/api/auth/jwt/create` и использовать его в запросах к корзине***
### 1-ый пример

Method: `POST`
Endpoint: `http://127.0.0.1:8000/api/shopping-cart/{product_pk}`

Body: 

```json
{
  "amount":  5
}
```

Response: 

```json
{
    "amount": 2,
    "user": "k",
    "id": 6,
    "product": "MacBook Pro"
}
```

Status code: 201


### 2-ой пример

Method: `GET`
Endpoint: `http:///127.0.0.1:8000/api/my-shopping-cart/view-my-cart`

Response: 

```json
{
    "cart_contents": [
        {
            "amount": 2,
            "product_name": "MacBook Pro",
            "product_price": 1999.99,
            "total_price": 3999.98
        },
        {
            "amount": 2,
            "product_name": "Мужская футболка",
            "product_price": 29.99,
            "total_price": 59.98
        }
    ],
    "total_items": 4,
    "total_price": 4059.96
}
```

Status code: 200


### 3-й пример

Method: `GET`
Endpoint: `http://127.0.0.1:8000/api/categories/?limit=2&offset=0`

Response: 

```json
{
  "count": 3,
  "next": "http://127.0.0.1:8000/api/categories/?limit=2&offset=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "image": "http://127.0.0.1:8000/media/categories/electronics.jpg",
      "slug": "electronics",
      "created_at": "2024-01-01T00:00:00Z",
      "title": "Электроника",
      "subcategories": [
        "Смартфоны",
        "Ноутбуки"
      ]
    },
    {
      "id": 2,
      "image": "http://127.0.0.1:8000/media/categories/clothing.jpg",
      "slug": "clothing",
      "created_at": "2024-01-01T00:00:00Z",
      "title": "Одежда",
      "subcategories": [
        "Мужская одежда",
        "Женская одежда"
      ]
    }
  ]
}
```

Status code: 200


### Использованные технологии

* Python 3.12
* Django 5.1.2
* Django REST framework 3.15.2
* djoser 2.2.3
* Sqlite3 
* Postgres

### Автор

[Кирилл Киселев](https://github.com/kirillkiselev-slim)

