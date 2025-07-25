from django.urls import path

from . import views

urlpatterns = [
     path("", views.index, name="index"),
    path("<str:entry>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("edit/", views.edit, name="edit"),
    path("update/", views.update, name="update"),
    path("random/", views.random, name="random")
]

