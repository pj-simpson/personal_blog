import pytest
from django.contrib.auth.models import Permission

from django.urls import reverse

from blog.models import Post
from users.models import CustomUser


# # # Fixtures # # #

@pytest.fixture(scope='function')
def add_user_no_permission():
    def _add_user(email,password):
        user = CustomUser.objects.create(email=email,
                          password=password)
        return user
    return _add_user

@pytest.fixture(scope='function')
def add_user_create_post():
    def _add_user(email,password):
        permission = Permission.objects.get(name='Can add post')
        user = CustomUser.objects.create(email=email,
                          password=password)
        user.user_permissions.add(permission)
        return user
    return _add_user

@pytest.fixture(scope='function')
def add_user_update_post():
    def _add_user(email,password):
        permission = Permission.objects.get(name='Can change post')
        user = CustomUser.objects.create(email=email,
                          password=password)
        user.user_permissions.add(permission)
        return user
    return _add_user

@pytest.fixture(scope='function')
def add_post():
    def _add_post(title,author,content):
        post = Post.objects.create(title=title,author=author,
                                   content=content)
        return post
    return _add_post


# # # Tests # # #

@pytest.mark.django_db
def test_post_list(add_user_no_permission,add_post):
    user = add_user_no_permission(email='regular@email.com', password='testpass123')
    post1 = add_post(title="test 1", author=user, content='test test test')
    post2 = add_post(title="test 2", author=user, content='test2 test2 test2')
#     test get list

@pytest.mark.django_db
def test_post_create(add_user_no_permission, add_user_create_post, add_post):
    user_no_permission = add_user_no_permission(email='regular@email.com', password='testpass123')
    user_permission = add_user_create_post(email='permmsion@email.com', password='testpass123')
    post1 = add_post(title="test 1", author=user_permission, content='test test test')
#     test get for perm and no perm
#       test post for perm

@pytest.mark.django_db
def test_post_detail(add_user_no_permission,add_post):
    user = add_user_no_permission(email='regular@email.com', password='testpass123')
    post1 = add_post(title="test 1", author=user, content='test test test')
#     test get detail

@pytest.mark.django_db
def test_post_edit(add_user_no_permission,add_user_update_post, add_post):
    user_no_permission = add_user_no_permission(email='regular@email.com', password='testpass123')
    user_permission = add_user_update_post(email='perm@email.com', password='testpass123')
    post1 = add_post(title="test 1", author=user_permission, content='test test test')
# test get for perm and no perm
# test post for perm
