import pytest


def test_customer_str(customer):
    assert customer.__str__() == "customer"


def test_customer_str(adminuser):
    assert adminuser.__str__() == "adminuser"


def test_customer_email_no_input(customer_factory):
    with pytest.raises(ValueError) as e:
        test = customer_factory.create(email='')
    assert str(e.value) == 'Customer account: Provide an Email to Continue'


def test_customer_emai_incorrect(customer_factory):
    with pytest.raises(ValueError) as e:
        test = customer_factory.create(email='a.com')
    assert str(e.value) == 'Provide an Email to Continue'


def test_adminuser_email_no_input(customer_factory):
    with pytest.raises(ValueError) as e:
        test = customer_factory.create(email='', is_superuser=True, is_staff=True)
    assert str(e.value) == 'Superuser account: Provide an Email to Continue'


def test_adminuser_emai_incorrect(customer_factory):
    with pytest.raises(ValueError) as e:
        test = customer_factory.create(email='a.com', is_superuser=True, is_staff=True)
    assert str(e.value) == 'Provide an Email to Continue'


def test_adminuser_email_not_staff(customer_factory):
    with pytest.raises(ValueError) as e:
        test = customer_factory.create(email='', is_superuser=True, is_staff=False)
    assert str(e.value) == 'Superuser Must Be Assined to is_staff=True'


def test_adminuser_email_not_superuser(customer_factory):
    with pytest.raises(ValueError) as e:
        test = customer_factory.create(email='a.com', is_superuser=False, is_staff=True)
    assert str(e.value) == 'Superuser Must Be Assined to is_superuser=True'


def test_address_str(address):
    name = address.full_name
    assert address.__str__() == name + "Address"
