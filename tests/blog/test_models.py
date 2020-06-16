import pytest

from blog.models import Post
from users.models import CustomUser

@pytest.fixture(scope='function')
def add_user():
    def _add_user(email,password):
        user = CustomUser.objects.create(email=email,
                          password=password)
        return user
    return _add_user

@pytest.fixture(scope='function')
def add_post():
    def _add_post(title,author,content):
        post = Post.objects.create(title=title,author=author,
                                   content=content)
        return post
    return _add_post

@pytest.mark.django_db
def test_post_model(add_user,add_post):
    user = add_user(email = 'testy@email.com',password = 'testpass123')
    post = add_post(title = "test",author = user,content = 'test test test')


    assert post.author == user
    assert post.created
    assert post.updated
    assert str(post) == post.title

@pytest.mark.django_db
def test_update_post_model(add_user,add_post):
    user = add_user(email = 'testy@email.com',password = 'testpass123')
    post = add_post(title = "test",author = user,content = 'test test test')

    assert str(post) == post.title
    assert post.content == 'test test test'

    Post.objects.filter(pk=post.pk).update(title='updated',content='update update update')
    post.refresh_from_db()

    assert post.title == 'updated'
    assert post.content == 'update update update'
    assert post.updated > post.created


