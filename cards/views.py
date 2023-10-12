import random
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
from django.contrib.auth.decorators import login_required

from .forms import CardCheckForm
from .models import Card


def sign_up(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        myuser = User.objects.create_user(username, email, password)

        myuser.save()

        messages.success(request, "Your account has been successfully created!")

        return redirect("card-list")
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
            messages.error(request, "Da Fuck Wut?")
            return redirect('card-list')
    return render(request, "registration/sign_in.html")

def sign_out(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect("card-list")
    

# @login_required
class CardListView(ListView):
    model = Card
    queryset = Card.objects.all().order_by("box", "-date_created")


# @login_required
class CardCreateView(CreateView):
    model = Card
    fields = ["question", "answer", "box", "image"]
    success_url = reverse_lazy("card-create")
    def form_valid(self, form):
        messages.success(self.request, "Updated Successfully",extra_tags='update')
        return super().form_valid(form)
    

# @login_required
class CardUpdateView(CardCreateView, UpdateView):
    success_url = reverse_lazy("card-list")


# @login_required
class CardDeleteView(DeleteView):
    model = Card
    template_name = "cards/card_confirm_delete.html"
    success_url = reverse_lazy("card-list")


# @login_required
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
