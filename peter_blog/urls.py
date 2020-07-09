from django.contrib import admin
from django.urls import include, path

from blog.views import AboutView, HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("crazy_admin_969/", admin.site.urls),
    path("blog/", include("blog.urls")),
    path("accounts/", include("allauth.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
]
