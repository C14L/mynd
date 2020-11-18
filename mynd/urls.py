from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from main import views

urlpatterns = [
    path(settings.URL_PREFIX + "sudo/", admin.site.urls),
    path(settings.URL_PREFIX + "login/", LoginView.as_view(), name="login"),
    path(settings.URL_PREFIX + "logout/", LogoutView.as_view(), name="logout"),
    path(settings.URL_PREFIX + "", views.home, name="home"),
    path(settings.URL_PREFIX + "add/", views.add, name="add"),
    path(settings.URL_PREFIX + "del/", views.delete, name="del"),
    path(settings.URL_PREFIX + "view/", views.view, name="view"),
    path(settings.URL_PREFIX + "diff/", views.diff, name="diff"),
]
