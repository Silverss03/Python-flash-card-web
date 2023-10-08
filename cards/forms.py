from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CardCheckForm(forms.Form):
    card_id = forms.IntegerField(required=True)
    solved = forms.BooleanField(required=False)
    ans = forms.CharField(max_length= 100, label= "Your answer")
    
class RegisterForm(UserCreationForm):   
    email = forms.EmailField(required= True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
