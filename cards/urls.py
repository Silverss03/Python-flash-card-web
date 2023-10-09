from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path("", views.CardListView.as_view(), name="card-list"),
    path("new", views.CardCreateView.as_view(), name="card-create"),
    path("edit/<int:pk>", views.CardUpdateView.as_view(), name="card-update"),
    path("box/<int:box_num>", views.BoxView.as_view(), name="box"),
    path("delete/<int:pk>", views.CardDeleteView.as_view(), name = "card-delete"),
    path("sign_up", views.UserRegistrationView.as_view(), name = "register"),
]

