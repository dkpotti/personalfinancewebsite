from django.urls import path
from . import views


urlpatterns = [
    path("", views.indexetfhome, name="indexetfhome"),
    path("add-fund.html", views.addfund, name="add-fund"),
]
