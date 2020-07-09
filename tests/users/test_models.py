import pytest
from pytest_django.fixtures import django_user_model


@pytest.mark.django_db
def test_user_model(add_user_no_permissions):
    user = add_user_no_permissions(username="testy@email.com", password="testpass123")

    assert user.username == "testy@email.com"
    assert user.password
