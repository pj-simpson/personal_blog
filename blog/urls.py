from django.urls import path

from .views import (
    drafts_list_view,
    portfolio_list_view,
    post_create_view,
    post_delete_view,
    post_detail_view,
    post_list_view,
    post_list_view_by_tag,
    post_update_view,
)

urlpatterns = [
    path("", post_list_view, name="post_list"),
    path("drafts", drafts_list_view, name="drafts"),
    path("portfolio", portfolio_list_view, name="portfolio"),
    path("tag/<slug:tag_slug>/", post_list_view_by_tag, name="post_list_by_tag"),
    path("create/", post_create_view, name="post_create"),
    path("<slug:slug>/", post_detail_view, name="post_detail"),
    path("edit/<uuid:pk>/", post_update_view, name="post_edit"),
    path("delete/<uuid:pk>/", post_delete_view, name="post_delete"),
]
