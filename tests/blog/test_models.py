import pytest

from blog.models import Post


@pytest.mark.django_db
def test_post_model(add_user_all_permissions, add_post):
    user = add_user_all_permissions(username="testy@email.com", password="testpass123")
    post = add_post(
        title="test test",
        author=user,
        content="test test test",
        headline="headline",
        draft=False,
    )
    post.tags.add("tag1")

    assert post.author == user
    assert post.created
    assert post.updated
    post_string = str(post)
    assert post_string == post.title
    assert "tag1" == post.tags.values()[0]["name"]
    assert post.slug == "test-test"


@pytest.mark.django_db
def test_update_post_model(add_user_all_permissions, add_post):
    user = add_user_all_permissions(username="testy@email.com", password="testpass123")
    post = add_post(
        title="test Two 3",
        author=user,
        content="test test test",
        headline="headline",
        draft=False,
    )
    post.tags.add("tag1")

    post_string = str(post)
    assert post_string == post.title
    assert post.content == "test test test"

    Post.objects.filter(pk=post.pk).update(
        title="Updated", content="update update update", draft=True
    )
    post.tags.set("tag3", clear=True)
    post.refresh_from_db()

    assert post.title == "Updated"
    assert post.content == "update update update"
    assert post.draft == True
    assert post.updated > post.created
    assert "tag3" == post.tags.values()[0]["name"]
    # slug doesnt update on save if already exists.
    assert post.slug == "test-two-3"
