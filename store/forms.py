from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Order

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
class Meta:
    model = User
    fields = ('username','email','password1','password2')

class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []  # extend with shipping/billing in real app