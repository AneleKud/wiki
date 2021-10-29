from django.urls import path

from . import views

#app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("pages/<str:title>", views.pages, name="pages"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("wikiedit/<str:title>", views.saveEdit, name="saveEdit"),
    path("new", views.NewArticle, name="new"),
    path("random", views.randomArticle, name="random"),
    path("search", views.search, name="search")
]