import pytest
from django.contrib.auth.models import Permission

from django.urls import reverse
from pytest_django.fixtures import django_user_model

from blog.models import Post
from users.models import CustomUser


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
    def _add_post(title,author,content,tags):
        post = Post.objects.create(title=title,author=author,
                                   content=content,tags=tags)
        return post
    return _add_post



# # # Tests # # #

@pytest.mark.django_db
def test_post_list(add_user_no_permissions,add_post,client):
    user = add_user_no_permissions(username='username', password='testpass123')
    post1 = add_post(title="test 1", author=user, content='test test test', tags='tag 1')
    post2 = add_post(title="test 2", author=user, content='test2 test2 test2', tags='tag 1')
    response = client.get(reverse('post_list'))
    assert response.status_code == 200
    assert 'test 1' in str(response.content)
    assert 'test2 test2 test2' in str(response.content)


@pytest.mark.django_db
def test_post_create_without_logged_in(client):
    response_1 = client.get(reverse('post_create'))
    assert response_1.status_code == 302

    response_2 = client.post(reverse('post_create'), data={"title": "test title", "content": "test content test test" ,"tags":"tag 1"})
    assert response_2.status_code == 302

@pytest.mark.django_db
def test_post_create_without_permissions(add_user_no_permissions,client):
    user = add_user_no_permissions(username='username', password='testpass123')
    client.login(username='username',password='testpass123')
    response_1 = client.get(reverse('post_create'))
    assert response_1.status_code == 403

    response_2 = client.post(reverse('post_create'), data={"title": "test title", "content": "test content test test","tags":"tag 1"})
    assert response_2.status_code == 403

@pytest.mark.django_db
def test_post_create_with_permissions(add_user_all_permissions, client):
    user = add_user_all_permissions(username='username', password='testpass123')
    client.login(username='username', password='testpass123')
    response_1 = client.get(reverse('post_create'))
    assert response_1.status_code == 200

    response_2 = client.post(reverse('post_create'), data={"title": "test title", "content": "test content test test","tags":"tag 1"})
    assert response_2.status_code == 302


@pytest.mark.django_db
def test_post_detail(add_user_all_permissions,add_post,client):
    user = add_user_all_permissions(username='username', password='testpass123')
    post = add_post(title="test 1", author=user, content='test test test', tags='tag 1')
    response = client.get(reverse('post_detail',kwargs={'pk': post.pk}))
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_edit_without_logged_in(add_user_all_permissions,add_post,client):
    user = add_user_all_permissions(username='username', password='testpass123')
    post = add_post(title="test 1", author=user, content='test test test', tags='tag 1')
    response_1 = client.get(reverse('post_edit',kwargs={'pk': post.pk}))
    assert response_1.status_code == 302

    response_2 = client.post(reverse('post_edit',kwargs={'pk': post.pk}), data={"title": "test title",
                                                                                "content": "test content test test","tags":"tag 1"})
    assert response_2.status_code == 302

@pytest.mark.django_db
def test_post_edit_without_permissions(add_user_all_permissions,add_user_no_permissions, add_post,client):
    user_all_permissions = add_user_all_permissions(username='username', password='testpass123')
    user_no_permissions = add_user_no_permissions(username='username_2', password='testpass123')
    post = add_post(title="test 1", author=user_all_permissions, content='test test test', tags='tag 1')
    client.login(username='username_2', password='testpass123')
    response_1 = client.get(reverse('post_edit', kwargs={'pk': post.pk}))
    assert response_1.status_code == 403

    response_2 = client.post(reverse('post_edit', kwargs={'pk': post.pk}),
                             data={"title": "test title", "content": "test content test test","tags":"tag 1"})
    assert response_2.status_code == 403

@pytest.mark.django_db
def test_post_edit_without_permissions(add_user_all_permissions, add_post,client):
    user_all_permissions = add_user_all_permissions(username='username', password='testpass123')
    post = add_post(title="test 1", author=user_all_permissions, content='test test test', tags='tag 1')
    client.login(username='username', password='testpass123')
    response_1 = client.get(reverse('post_edit', kwargs={'pk': post.pk}))
    assert response_1.status_code == 200

    response_2 = client.post(reverse('post_edit', kwargs={'pk': post.pk}),
                             data={"title": "test title", "content": "test content test test","tags":"tag 1"})
    assert response_2.status_code == 302

