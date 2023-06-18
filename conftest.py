import pytest
from pytest_factoryboy import register
from backend.tests.factories import (
    CategoryFactory,
    ProductTypeFactory,
    ProductSpecificationFactory,
    AddressFactory,
    CustomerFactory,
    ProductFactory
)

register(CategoryFactory)
register(ProductTypeFactory)
register(ProductSpecificationFactory)
register(ProductFactory)
register(CustomerFactory)
register(AddressFactory)


@pytest.fixture
def product_category(db, Category_factory):
    category = Category_factory.create()
    return category


@pytest.fixture
def product_type(db, product_type_factory):
    product_type = product_type_factory.create()
    return product_type


@pytest.fixture
def product_specification(db, product_specification_factory):
    product_spec = product_specification_factory.create()
    return product_spec


@pytest.fixture
def product(db, product_factory):
    product_spec = product_factory.create()
    return product_spec


@pytest.fixture
def customer(db, customer_factory):
    new_customer = customer_factory.create()
    return new_customer


@pytest.fixture
def adminuser(db, customer_factory):
    new_customer = customer_factory.create(name='admin_user', is_staff=True, is_superuser=True)
    return new_customer