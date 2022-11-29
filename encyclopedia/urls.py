from django.urls import path

from . import views

app_name="encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.get_content, name="get_content"),
    path("search/", views.search, name="search"),
    path("create/", views.creating, name="create"),
    path("edit/<str:title>", views.initialize_form, name="initialize_form"),
    path("edit/", views.editing, name="edit_post"),
    path("random/", views.random_pages, name="random_entry"),
]
