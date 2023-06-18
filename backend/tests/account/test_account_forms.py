import pytest
from backend.apps.account.forms import RegisterationForm, UserAddressForm


@pytest.mark.parametrize(
    'full_name, phone, post_code, address_line, address_line_2, town_city',
    ("mikael", '023659889', 'add1', 'add2', 'town', 'postcode', False),
    ("dimitri", '023659889', 'add1', 'add2', 'town', 'postcode', True)
)
def test_customer_add(full_name, phone, post_code, address_line, address_line_2, town_city, validity):
    form = UserAddressForm(
        data={
            "full_name": full_name,
            "phone": phone,
            "post_code": post_code,
            "address_line": address_line,
            "address_line_2": address_line_2,
            "town_city": town_city

        }
    )
    assert form.is_valid() is validity


def test_customer_create_address(client, customer):
    user = customer
    client.force_login(user)
    response = client.post('/account/add_address/', data={"full_name": "name"})
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_account(user_name, email, password, password2, validity):
    form = RegisterationForm(
        data={
            "user_name": user_name,
            "email": email,
            "password": password,
            "password2": password2,
        }
    )
    assert form.is_valid() is validity


@pytest.mark.parametrize(
    'user_name, email, password, password2, validity',
    [
        ("mikael", '0236@59889.com', '123', 200),
        ("dimitri", '0236@59889.com', '321', 522),
    ],
)
@pytest.mark.django_db
def test_create_account_view(client, user_name, email, password, password2, validity):
    response = client.post(
        'account/register/',
        data={
            "user_name": user_name,
            "email": email,
            "password": password,
            "password2": password2
        },
    )


def test_account_register_redirect(client, customer):
    user = customer
    client.force_login(user)
    response = client.get('/account/register/')
    assert response.status_code == 302


def test_account_register_render(client):
    response = client.get('/account/register/')
    assert response.status_code == 200
