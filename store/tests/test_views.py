from unittest import skip

from django.test import TestCase

from django.contrib.auth.models import User
from store.models import Category, Product

@skip("demostrating skip")
class TestSkip(TestCase):
    def test_skip_example(self):
        pass
