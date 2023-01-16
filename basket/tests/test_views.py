from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from store.models import Product, Category


class TestBasketView(TestCase):
    def setUp(self):
        User.objects.create(username='admin')
        Category.objects.create(name='django', slug='django')
        Product.objects.create(category_id=1, title='django beginners',
                                            image='django', slug='django-beginners',
                                            price=40.00, created_by_id=1)
        Product.objects.create(category_id=1, title='django intermediate',
                                            image='django', slug='django-intermediate',
                                            price=40.00, created_by_id=1)
        Product.objects.create(category_id=1, title='django advanced',
                                            image='django', slug='django-advanced',
                                            price=40.00, created_by_id=1)
        self.client.post(
            reverse('basket:basket_add'), {"productid": 3, 'productqty': 1, "action": "post"}, xhr=True
        )
        self.client.post(
            reverse('basket:basket_add'), {"productid": 2, 'productqty': 2, "action": "post"}, xhr=True
        )


    def test_basket_url(self):
        response = self.client.get(reverse('basket:basket_summary'))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        response = self.client.post(
            reverse('basket:basket_add'), {"productid": 3, 'productqty': 1, "action": "post"}, xhr=True
        )
        self.assertEqual(response.json(), {'quantity': 4})
        response = self.client.post(
            reverse('basket:basket_add'), {"productid": 2, 'productqty': 1, "action": "post"}, xhr=True
        )
        self.assertEqual(response.json(), {'quantity': 3})

    def test_basket_delete(self):
        response = self.client.post(
            reverse('basket:basket_delete'), {"productid": 2, "action": "post"}, xhr=True
        )
        self.assertEqual(response.json(), {'quantity': 1, 'subtotal': '40.00'})

def test_basket_update(self):
        response = self.client.post(
            reverse('basket:basket_update'), {"productid": 2, "productqty": 1, "action": "post"}, xhr=True
        )
        self.assertEqual(response.json(), {'quantity': 2, 'subtotal': '80.00'})

