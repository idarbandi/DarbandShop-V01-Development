import factory
from backend.apps.catalogue.models import Category, ProductType, ProductSpecification, Product
from backend.apps.account.models import CustomAccountManager, Customer, Address
from faker import Faker

fake = Faker()

"""
    Catalogue
"""


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "digital"
    slug = "digital"


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType
        django_get_or_create = ("name",)

    name = factory.sequence(lambda n: f'Book {0}'.format(n))


class ProductSpecificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSpecification

    name = "digital"
    product_type = factory.SubFactory(ProductTypeFactory)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    product_type = factory.SubFactory(ProductTypeFactory)
    category = factory.SubFactory(CategoryFactory)
    title = 'product_title'
    description = fake.next()
    slug = 'product_slug'
    regular_price = '9.99'
    discount_price = '4.99'


"""
    Account
"""


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    email = "d@s.com"
    name = 'customer'
    mobile = '032658999'
    password = 'test'
    is_active = True
    is_staff = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    customer = factory.SubFactory(CustomerFactory)
    full_name = fake.name()
    phone = fake.phone_number()
    postcode = fake.postcode()
    address_line = fake.street_address()
    address_line2 = fake.street_address()
    town_city = fake.city_suffix()

