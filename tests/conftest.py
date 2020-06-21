import pytest

from pytest_django.fixtures import django_user_model

from blog.models import Post
# # # Fixtures # # #

@pytest.fixture(scope='function')
def add_user_no_permissions(django_user_model):
    def _add_user_no_permissions(username,password):
        user = django_user_model.objects.create_user(username=username, password=password)
        return user
    return _add_user_no_permissions

@pytest.fixture(scope='function')
def add_user_all_permissions(django_user_model):
    def _add_user_all_permissions(username,password):
        user = django_user_model.objects.create_superuser(username=username, password=password)
        return user
    return _add_user_all_permissions

@pytest.fixture(scope='function')
def add_post():
    def _add_post(title,author,content):
        post = Post.objects.create(title=title,author=author,
                                   content=content)
        return post
    return _add_post