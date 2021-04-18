from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("newpage", views.create, name="create"),
    path("edit", views.edit, name="edit"),
    path("search", views.searchq, name="search"),
    path("randomp", views.randomp, name="random")
]
