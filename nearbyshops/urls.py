from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


    # API Routes
    path("fetch_data/<str:john_location>", views.get_data, name="fetch_data"),
    path("review", views.review, name="review"),
    path("reverse_geocode", views.reverse_geocode, name="reverse_geocode"),
    path("add_new_john", views.add_new_john, name="add_new_john"),
]