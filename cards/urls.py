from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path("", login_required(views.CardListView.as_view()), name="card-list"),
    path("new", views.CardCreateView.as_view(), name="card-create"),
    path("edit/<int:pk>", views.CardUpdateView.as_view(), name="card-update"),
    path("box/<int:box_num>", views.BoxView.as_view(), name="box"),
    path("delete/<int:pk>", views.CardDeleteView.as_view(), name = "card-delete"),
    path("sign_up", views.sign_up, name = "sign-up"),
    path("sign_in", views.sign_in, name = "sign-in"),
    path("sign_out", views.sign_out, name = "sign-out"),
]

