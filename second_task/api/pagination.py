from rest_framework.pagination import LimitOffsetPagination


class SarafanPageNumberPagination(LimitOffsetPagination):
    max_page_size = 100
