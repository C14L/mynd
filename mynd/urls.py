from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from main import views

urlpatterns = [
    path("sudo/", admin.site.urls),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", views.home, name="home"),
    path("add/", views.add, name="add"),
    path("del/", views.delete, name="del"),
    path("view/", views.view, name="view"),
    path("diff/", views.diff, name="diff"),
]
