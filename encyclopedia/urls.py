from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="page"),
    path("search", views.search, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random/", views.rand, name="rand")
]
