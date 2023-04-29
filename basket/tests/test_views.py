from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from store.models import Category, Product


class TestBasketView(TestCase):
    def setUp(self) -> None:
        User.objects.create(username="admin")
        Category.objects.create(name="django", slug="django")
        Product.objects.create(category_id=1, title="django", created_by_id=1,
                               slug="django", price="20.00", image="django")
        Product.objects.create(category_id=1, title="django_one", created_by_id=1,
                               slug="django-one", price="20.00", image="django")
        Product.objects.create(category_id=1, title="django_two", created_by_id=1,
                               slug="django-two", price="20.00", image="django")

        self.client.post(
            reverse("basket:basket_add"), {"productid": 1, "productqty": 1, "action": "post"}, xhr=True
        )
        self.client.post(
            reverse("basket:basket_add"), {"productid": 2, "productqty": 2, "action": "post"}, xhr=True
        )

    def test_basket_url(self):
        """
            basket main url
        """
        response = self.client.get(reverse("basket:basket_summary"))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        """
            test adding items to the basket
        """
        response = self.client.post(
            reverse("basket:basket_add"), {"productid": 3, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {"qty": 4})

    def test_basket_delete(self):
        """
            test deleting items for basket
        """
        response = self.client.post(
            reverse("basket:basket_delete"), {"productid": 2, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 1, 'subtotal': '20.00'})

    def test_basket_update(self):
        """
            test update items
        """
        response = self.client.post(
            reverse("basket:basket_update"), {"productid": 2, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 2, 'subtotal': '40.00'})

