import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_url_root(client):
    url = reverse("catalogue:home")
    response = client.get(url)
    assert response.status_code == 200
