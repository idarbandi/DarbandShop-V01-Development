from importlib import import_module
from django.test import TestCase
from unittest import skip
from django.contrib.auth.models import User

from backend import settings
from store.models import Category, Product
from django.urls import reverse
from django.test import Client, RequestFactory, TestCase
from store.views import products
from django.http import HttpRequest


class TestViewResponse(TestCase):
    def setUp(self) -> None:
        self.c = Client()
        self.factory = RequestFactory()
        User.objects.create(username="admin")
        Category.objects.create(name="digital", slug="digital")
        Product.objects.create(category_id=1, title="digital", created_by_id=1,
                               slug="digital", price="20.00", image="digital")

    def test_url_allowed_hosts(self):
        """
            Test Allowed Hosts
        """
        response = self.c.get("/")
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        response = self.c.get(reverse("store:product_detail", args=["digital"]))
        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        response = self.c.get(reverse("store:category_detail", args=["digital"]))
        self.assertEqual(response.status_code, 200)

    @skip("no session")
    def test_home_page_url(self):
        """
            Test & See If Main page Returns The Result
        """
        request = HttpRequest()
        response = products(request)
        html = response.content.decode("utf8")
        self.assertIn("<title>Home</title>", html)
        self.assertTrue(html.startswith("<!doctype html>"))
        self.assertEqual(response.status_code, 200)
