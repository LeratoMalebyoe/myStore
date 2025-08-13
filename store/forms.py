from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Order


class SignUpForm(UserCreationForm):
    """
    Form for creating a new user account.

    Inherits from:
        UserCreationForm: Provides username and password fields.

    Additional fields:
        email (EmailField): Required email address for the user.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CartAddForm(forms.Form):
    """
    Form for adding a product to the cart.

    Fields:
        quantity (IntegerField): The number of units to add, must be at least 1.
    """
    quantity = forms.IntegerField(min_value=1, initial=1)


class CheckoutForm(forms.ModelForm):
    """
    Form for processing checkout.

    Meta:
        model (Order): The associated order model.
        fields (list): Currently empty, but can be extended with
        shipping/billing fields in a real application.
    """
    class Meta:
        model = Order
        fields = []  # extend with shipping/billing in real app
