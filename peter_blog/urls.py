from django.contrib import admin
from django.urls import path, include

from users.views import HomePageView

urlpatterns = [
    path('',HomePageView.as_view(), name='home'),
    path('crazy_admin_969/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('accounts/', include('allauth.urls')),
    path("ckeditor/", include("ckeditor_uploader.urls")),
]
