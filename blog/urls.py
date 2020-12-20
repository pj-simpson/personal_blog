from django.urls import path

from .views import (post_create_view, post_detail_view, post_list_view,
                    post_list_view_by_tag, post_update_view)

urlpatterns = [
    path("", post_list_view, name="post_list"),
    path("tag/<slug:tag_slug>/", post_list_view_by_tag, name="post_list_by_tag"),
    path("create/", post_create_view, name="post_create"),
    path("<uuid:pk>/", post_detail_view, name="post_detail"),
    path("edit/<uuid:pk>/", post_update_view, name="post_edit"),
]
