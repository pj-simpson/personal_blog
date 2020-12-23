import pytest

from django.urls import reverse
from pytest_django.fixtures import django_user_model

from taggit.models import Tag


@pytest.mark.django_db
def test_post_list(add_user_all_permissions, add_post, client):
    user = add_user_all_permissions(username="username", password="testpass123")
    post1 = add_post(
        title="test 1",
        author=user,
        content="test test test",
        headline="headline",
        draft=False,
    )
    post2 = add_post(
        title="test 2", author=user, content="test 2", headline="headline", draft=False
    )
    response = client.get(reverse("post_list"))
    assert response.status_code == 200
    assert "test 1" in str(response.content)
    assert "test 2" in str(response.content)


@pytest.mark.django_db
def test_draft_list_logged_in_can_see_drafts(
    add_user_all_permissions, add_post, client
):
    user = add_user_all_permissions(username="username", password="testpass123")
    client.login(username="username", password="testpass123")
    post1 = add_post(
        title="test 1",
        author=user,
        content="test test test",
        headline="headline",
        draft=True,
    )
    post2 = add_post(
        title="test 2",
        author=user,
        content="test2 test2 test2",
        headline="headline",
        draft=True,
    )
    response = client.get(reverse("drafts"))
    assert response.status_code == 200
    assert "test 1" in str(response.content)
    assert "test 2" in str(response.content)


@pytest.mark.django_db
def test_draft_list_not_logged_gets_redirected(
    add_user_all_permissions, add_user_no_permissions, add_post, client
):
    user = add_user_all_permissions(username="username", password="testpass123")
    user = add_user_no_permissions(username="username1", password="testpass1234")
    client.login(username="username1", password="testpass1234")
    post1 = add_post(
        title="test 1",
        author=user,
        content="test test test",
        headline="headline",
        draft=True,
    )
    post2 = add_post(
        title="test 2",
        author=user,
        content="test2 test2 test2",
        headline="headline",
        draft=True,
    )
    response = client.get(reverse("drafts"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_post_list_with_tags(add_user_all_permissions, add_post, client):
    user = add_user_all_permissions(username="username", password="testpass123")
    post1 = add_post(
        title="test 1",
        author=user,
        content="test test test",
        headline="headline",
        draft=False,
    )
    post2 = add_post(
        title="test 2",
        author=user,
        content="test2 test2 test2",
        headline="headline",
        draft=False,
    )
    post1.tags.add("tag1")
    post2.tags.add("tag2")
    response = client.get(reverse("post_list_by_tag", kwargs={"tag_slug": "tag1"}))
    assert response.status_code == 200
    assert "test 1" in str(response.content)
    assert "test2 test2 test2" not in str(response.content)


@pytest.mark.django_db
def test_post_list_with_tags_logged_in_can_see_drafts(
    add_user_all_permissions, add_post, client
):
    user = add_user_all_permissions(username="username", password="testpass123")
    client.login(username="username", password="testpass123")
    post1 = add_post(
        title="test 1",
        author=user,
        content="test test test",
        headline="headline",
        draft=False,
    )
    post2 = add_post(
        title="test 2",
        author=user,
        content="test2 test2 test2",
        headline="headline",
        draft=True,
    )
    post1.tags.add("tag1")
    post2.tags.add("tag2")
    response = client.get(reverse("post_list_by_tag", kwargs={"tag_slug": "tag1"}))
    assert response.status_code == 200
    assert "test 1" in str(response.content)
    assert "test2 test2 test2" not in str(response.content)


@pytest.mark.django_db
def test_post_list_with_tags_not_logged_in_cannot_see_drafts(
    add_user_all_permissions, add_user_no_permissions, add_post, client
):
    user = add_user_all_permissions(username="username", password="testpass123")
    post1 = add_post(
        title="test 1",
        author=user,
        content="test test test",
        headline="headline",
        draft=True,
    )
    post2 = add_post(
        title="test 2",
        author=user,
        content="test2 test2 test2",
        headline="headline",
        draft=True,
    )
    post1.tags.add("tag1")
    post2.tags.add("tag2")
    response = client.get(reverse("post_list_by_tag", kwargs={"tag_slug": "tag1"}))
    assert response.status_code == 200
    assert "test 1" not in str(response.content)
    assert "test2 test2 test2" not in str(response.content)


@pytest.mark.django_db
def test_post_list_with_non_existent_tags(add_user_all_permissions, add_post, client):
    user = add_user_all_permissions(username="username", password="testpass123")
    post1 = add_post(
        title="test 1",
        author=user,
        content="test test test",
        headline="headline",
        draft=False,
    )
    post1.tags.add("tag1")
    response = client.get(
        reverse("post_list_by_tag", kwargs={"tag_slug": "tag_2_blah"})
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_list_with_existent_tag_without_posts(client):
    Tag.objects.get_or_create(name="tag_1")
    response = client.get(reverse("post_list_by_tag", kwargs={"tag_slug": "tag_1"}))
    assert response.status_code == 200
    assert "No posts yet..." in str(response.content)


@pytest.mark.django_db
def test_post_create_without_logged_in(client):
    response_1 = client.get(reverse("post_create"))
    assert response_1.status_code == 302

    response_2 = client.post(
        reverse("post_create"),
        data={
            "title": "test title",
            "content": "test content test test",
            "tags": "tag 1",
            "headline": "headline",
            "draft": False,
        },
    )
    assert response_2.status_code == 302


@pytest.mark.django_db
def test_post_create_without_permissions(add_user_no_permissions, client):
    user = add_user_no_permissions(username="username1", password="testpass1234")
    client.login(username="username1", password="testpass1234")
    response_1 = client.get(reverse("post_create"))
    assert response_1.status_code == 302

    response_2 = client.post(
        reverse("post_create"),
        data={
            "title": "test title",
            "content": "test content test test",
            "tags": "tag 1",
            "headline": "headline",
            "draft": False,
        },
    )
    assert response_2.status_code == 302


@pytest.mark.django_db
def test_post_create_with_permissions(add_user_all_permissions, client):
    user = add_user_all_permissions(username="username", password="testpass123")
    client.login(username="username", password="testpass123")
    response_1 = client.get(reverse("post_create"))
    assert response_1.status_code == 200

    response_2 = client.post(
        reverse("post_create"),
        data={
            "title": "test title",
            "content": "test content test test",
            "tags": "tag 1",
            "headline": "headline",
            "draft": False,
        },
    )
    assert response_2.status_code == 302


@pytest.mark.django_db
def test_post_detail(add_user_all_permissions, add_post, client):
    user = add_user_all_permissions(username="username", password="testpass123")
    post = add_post(
        title="test 1",
        author=user,
        content="test test test",
        headline="headline",
        draft=False,
    )
    response = client.get(reverse("post_detail", kwargs={"pk": post.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_edit_without_logged_in(add_user_all_permissions, add_post, client):
    user = add_user_all_permissions(username="username", password="testpass123")
    post = add_post(
        title="test 1",
        author=user,
        content="test test test",
        headline="headline",
        draft=False,
    )
    response_1 = client.get(reverse("post_edit", kwargs={"pk": post.pk}))
    assert response_1.status_code == 302

    response_2 = client.post(
        reverse("post_edit", kwargs={"pk": post.pk}),
        data={
            "title": "test title",
            "content": "test content test test",
            "tags": "tag 1",
            "headline": "headline",
            "draft": False,
        },
    )
    assert response_2.status_code == 302


@pytest.mark.django_db
def test_post_edit_without_permissions(
    add_user_all_permissions, add_user_no_permissions, add_post, client
):
    user_all_permissions = add_user_all_permissions(
        username="username", password="testpass123"
    )
    user_no_permissions = add_user_no_permissions(
        username="username_2", password="testpass123"
    )
    post = add_post(
        title="test 1",
        author=user_all_permissions,
        content="test test test",
        headline="headline",
        draft=False,
    )
    client.login(username="username_2", password="testpass123")
    response_1 = client.get(reverse("post_edit", kwargs={"pk": post.pk}))
    assert response_1.status_code == 302

    response_2 = client.post(
        reverse("post_edit", kwargs={"pk": post.pk}),
        data={
            "title": "test title",
            "content": "test content test test",
            "tags": "tag 1",
            "headline": "headline",
            "draft": False,
        },
    )
    assert response_2.status_code == 302
    response_3 = client.get(reverse("post_detail", kwargs={"pk": post.pk}))
    assert "test title" not in str(response_3.content)


@pytest.mark.django_db
def test_post_edit_with_permissions(add_user_all_permissions, add_post, client):
    user_all_permissions = add_user_all_permissions(
        username="username", password="testpass123"
    )
    post = add_post(
        title="test 1",
        author=user_all_permissions,
        content="test test test",
        headline="headline",
        draft=False,
    )
    client.login(username="username", password="testpass123")
    response_1 = client.get(reverse("post_edit", kwargs={"pk": post.pk}))
    assert response_1.status_code == 200

    response_2 = client.post(
        reverse("post_edit", kwargs={"pk": post.pk}),
        data={
            "title": "test title",
            "content": "test content test test",
            "tags": "tag 1",
            "headline": "headline",
            "draft": False,
        },
    )
    assert response_2.status_code == 302


####### DELETION TESTS


@pytest.mark.django_db
def test_post_delete_without_logged_in(add_user_all_permissions, add_post, client):
    user = add_user_all_permissions(username="username", password="testpass123")
    post = add_post(
        title="test 1",
        author=user,
        content="test test test",
        headline="headline",
        draft=False,
    )
    response_1 = client.get(reverse("post_delete", kwargs={"pk": post.pk}))
    assert response_1.status_code == 302

    response_2 = client.post(reverse("post_delete", kwargs={"pk": post.pk}))
    assert response_2.status_code == 302


@pytest.mark.django_db
def test_post_delete_without_permissions(
    add_user_all_permissions, add_user_no_permissions, add_post, client
):
    user_all_permissions = add_user_all_permissions(
        username="username", password="testpass123"
    )
    user_no_permissions = add_user_no_permissions(
        username="username_2", password="testpass123"
    )
    post = add_post(
        title="test 1",
        author=user_all_permissions,
        content="test test test",
        headline="headline",
        draft=False,
    )
    client.login(username="username_2", password="testpass123")
    response_1 = client.get(reverse("post_delete", kwargs={"pk": post.pk}))
    assert response_1.status_code == 302
    response_2 = client.get(reverse("post_detail", kwargs={"pk": post.pk}))
    assert response_2.status_code == 200


@pytest.mark.django_db
def test_post_delete_with_permissions(add_user_all_permissions, add_post, client):
    user_all_permissions = add_user_all_permissions(
        username="username", password="testpass123"
    )
    post = add_post(
        title="test 1",
        author=user_all_permissions,
        content="test test test",
        headline="headline",
        draft=False,
    )
    client.login(username="username", password="testpass123")
    response_1 = client.get(reverse("post_delete", kwargs={"pk": post.pk}))
    assert response_1.status_code == 302
    response_2 = client.get(reverse("post_detail", kwargs={"pk": post.pk}))
    assert response_2.status_code == 404
