from importlib import import_module
from unittest import skip

from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.conf import settings

from store.models import Category, Product
from store.views import product_all

# @skip("demostrating skip")
# class TestSkip(TestCase):
#     def test_skip_example(self):
#         pass

class TestViewResponse(TestCase):
    def setUp(self) -> None:
        self.c = Client()
        Category.objects.create(name='django', slug='django')
        User.objects.create(username='admin')
        self.data1 = Product.objects.create(category_id=1, title='django beginners',
                                            image='django', slug='django-beginners',
                                            price=40.00, created_by_id=1)

    def test_url_allowed_host(self):
        """
        Test allowed Hosts
        """
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.c.get('/', HTTP_HOST='abcd.com')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """
        Test Product Details
        """
        response = self.c.get(reverse('store:product_detail', args=['django-beginners']))
        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        """
        Test Category Details
        """
        response = self.c.get(reverse('store:category_list', args=['django']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """
        Test homepage html
        """
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>BookStore</title>', html)
        self.assertTrue('\n<!doctype html>\n')
        self.assertEqual(response.status_code, 200)

