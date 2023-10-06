import random
from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import CardCheckForm
from .forms import RegisterForm
from .models import Card

class UserRegistrationView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/sign_up.html'
    def post(self, request, *args: str, **kwargs: Any) :
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
        return redirect(reverse_lazy("card-list"))
class CardListView(ListView):
    model = Card
    queryset = Card.objects.all().order_by("box", "-date_created")


class CardCreateView(CreateView):
    model = Card
    fields = ["question", "answer", "box"]
    success_url = reverse_lazy("card-create")
    def form_valid(self, form):
        messages.success(self.request, "Updated Successfully")
        return super().form_valid(form)


class CardUpdateView(CardCreateView, UpdateView):
    success_url = reverse_lazy("card-list")

class CardDeleteView(DeleteView):
    model = Card
    template_name = "cards/card_confirm_delete.html"
    success_url = reverse_lazy("card-list")


class BoxView(CardListView):
    template_name = "cards/box.html"
    form_class = CardCheckForm 
    def get_queryset(self):
        return Card.objects.filter(box=self.kwargs["box_num"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["box_number"] = self.kwargs["box_num"]
        if self.object_list:
            context["check_card"] = random.choice(self.object_list)
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            card = get_object_or_404(Card, id=form.cleaned_data["card_id"])
            if(str(form.cleaned_data["ans"]).lower() == card.answer.lower().strip()):
                form.cleaned_data["solved"] = True
                card.move(form.cleaned_data["solved"]) 
            else:
                card.move(form.cleaned_data["solved"])            
        return redirect(request.META.get("HTTP_REFERER"))
