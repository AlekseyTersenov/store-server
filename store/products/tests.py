import os
from http import HTTPStatus

import django
from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
django.setup()


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertEqual(response.template_name, ["products/index.html"])


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def setUp(self):
        self.products = Product.objects.all()

    def test_view(self):
        path = reverse('products:index')
        response = self.client.get(path)
        paginate_by = response.context_data['paginator'].per_page

        self._common_tests(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:paginate_by]))

    def test_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_ID': category.id})
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id))
        )

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertEqual(response.template_name[0], "products/products.html")
