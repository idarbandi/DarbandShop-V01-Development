from django.test import TestCase
from django.contrib.auth.models import User
from store.models import Category, Product


class TestCategoriesModel(TestCase):

    def setUp(self) -> None:
        self.data1 = Category.objects.create(name="django", slug="django")

    def test_category_model_entry(self):
        """
        Test Model categories data Insertion /type/field/attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))


class TestProductModel(TestCase):
    def setUp(self) -> None:
        Category.objects.create(name="django", slug="django")
        User.objects.create(username="admin")
        self.data1 = Product.objects.create(category_id=1, title="django", created_by_id=1,
                                            slug="django", price=12.00, image="django")

    def test_products_model_entry(self):
        """
        Test Model Product Default Name
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), "django")
