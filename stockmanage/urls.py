from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("add-stock.html", views.addstock, name="add-stock"),
]
