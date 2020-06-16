from django.urls import path

from .views import PostListView,PostDetailView,PostUpdateView, PostCreateView

urlpatterns = [
    path('', PostListView.as_view(), name="post_list"),
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("<uuid:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("edit/<uuid:pk>/",PostUpdateView.as_view() , name="post_edit"),
]

