import random
from typing import Any
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CardCheckForm
from .models import Card


def sign_up(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            error_message = "Passwords do not match."
            return render(request, "registration/sign_up.html", {"error_message": error_message})

        if User.objects.filter(username = username).exists() or User.objects.filter(email = email).exists():
            error_message = "Account with this username or email already exists."
            return render(request, "registration/sign_up.html", {"error_message": error_message})
        
        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        
        user = authenticate(username = username, password = password)        
        login(request, user)
        return render(request, "cards/base.html")
        
    return render(request, "registration/sign_up.html")
    
def sign_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            return render(request, "cards/base.html")
        else:
            error_message =  "Your username or password is wrong."
            return render(request, "registration/sign_in.html", {"error_message": error_message})
    return render(request, "registration/sign_in.html")

def sign_out(request):
    logout(request)
    return redirect("card-list")
    

# @login_required
class CardListView(LoginRequiredMixin,ListView):
    model = Card
    def get_queryset(self) :
        return Card.objects.filter(user = self.request.user).order_by("box", "-date_created")


# @login_required
class CardCreateView(LoginRequiredMixin,CreateView):
    model = Card
    fields = ["question", "answer", "box", "image"]
    success_url = reverse_lazy("card-create")
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

# @login_required
class CardUpdateView(CardCreateView, UpdateView, LoginRequiredMixin):
    success_url = reverse_lazy("card-list")
    def get_queryset(self) :
        return Card.objects.filter(user = self.request.user)
    


# @login_required
class CardDeleteView(DeleteView,LoginRequiredMixin):
    model = Card
    template_name = "cards/card_confirm_delete.html"
    success_url = reverse_lazy("card-list")


# @login_required
class BoxView(CardListView,LoginRequiredMixin):
    template_name = "cards/box.html"
    form_class = CardCheckForm 
    def get_queryset(self):
        return Card.objects.filter(box=self.kwargs["box_num"],user = self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["box_number"] = self.kwargs["box_num"]
        box_num = self.kwargs["box_num"]
        user_card_count = Card.objects.filter(user = self.request.user, box= box_num).count()
        context["user_card_count"] = user_card_count
        if self.object_list:
            context["check_card"] = random.choice(self.object_list)
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            card = get_object_or_404(Card, id=form.cleaned_data["card_id"])
            arr = str(form.cleaned_data["ans"]).lower().strip().split()
            ans = ""
            for i in arr :
                ans += i + " "
            arr2 = card.answer.lower().strip().split()
            def_ans = ""
            for i in arr2 :
                def_ans+= i + " "
            if(ans.strip() == def_ans.strip()):
                form.cleaned_data["solved"] = True
                messages.success(self.request, "Correct answer",extra_tags='correct_ans')
                card.move(form.cleaned_data["solved"]) 
            else:
                messages.success(self.request, "Wrong answer!!",extra_tags='wrong_ans')
                card.move(form.cleaned_data["solved"])            
        return redirect(request.META.get("HTTP_REFERER"))
