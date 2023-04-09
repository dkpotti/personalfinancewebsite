from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("add-money.html", views.addmoney, name="add-money"),
]
