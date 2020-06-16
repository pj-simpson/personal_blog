import pytest

from users.models import CustomUser


@pytest.mark.django_db
def test_movie_model():
    user = CustomUser(email='testy@email.com',
            password='testpass123')
    user.save()
    assert user.email == "testy@email.com"
    assert user.password == "testpass123"


