import pytest

from blog.models import Post


@pytest.mark.django_db
def test_post_model(add_user_all_permissions, add_post):
    user = add_user_all_permissions(username="testy@email.com", password="testpass123")
    post = add_post(title="test", author=user, content="test test test")
    post.tags.add("tag1")

    assert post.author == user
    assert post.created
    assert post.updated
    post_string = str(post)
    assert post_string == post.title
    assert "tag1" == post.tags.values()[0]["name"]


@pytest.mark.django_db
def test_update_post_model(add_user_all_permissions, add_post):
    user = add_user_all_permissions(username="testy@email.com", password="testpass123")
    post = add_post(title="test", author=user, content="test test test")
    post.tags.add("tag1")

    post_string = str(post)
    assert post_string == post.title
    assert post.content == "test test test"

    Post.objects.filter(pk=post.pk).update(
        title="updated", content="update update update"
    )
    post.tags.set("tag3", clear=True)
    post.refresh_from_db()

    assert post.title == "updated"
    assert post.content == "update update update"
    assert post.updated > post.created
    assert "tag3" == post.tags.values()[0]["name"]
