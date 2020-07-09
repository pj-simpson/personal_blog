from django.urls import path

from .views import PostCreateView, PostDetailView, PostListView, PostUpdateView

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("tag/<slug:tag_slug>/", PostListView.as_view(), name="post_list_by_tag"),
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("<uuid:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("edit/<uuid:pk>/", PostUpdateView.as_view(), name="post_edit"),
]
