from django import forms


class CardCheckForm(forms.Form):
    card_id = forms.IntegerField(required=True)
    solved = forms.BooleanField(required=False)
    ans = forms.CharField(max_length= 100, label= "Your answer")

