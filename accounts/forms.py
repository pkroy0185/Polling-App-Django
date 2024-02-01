from django import forms
from django.contrib.auth.models import User
from .models import StaffUser
# from .models import PaymentMethod
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        
class StaffUserRegistrationForm(UserCreationForm):
    card_number = forms.CharField(max_length=16, required=True)
    cardholder_name = forms.CharField(max_length=255, required=True)
    expiration_date = forms.DateField(required=True)
    cvv = forms.CharField(max_length=4, required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'card_number', 'cardholder_name', 'expiration_date', 'cvv']

# class UserRegistrationForm(forms.Form):
#     username = forms.CharField(label='Username', max_length=100, min_length=5,
#                                widget=forms.TextInput(attrs={'class': 'form-control'}))
#     email = forms.EmailField(label='Email', max_length=35, min_length=5,
#                              widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     password1 = forms.CharField(label='Password', max_length=50, min_length=5,
#                                 widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     password2 = forms.CharField(label='Confirm Password',
#                                 max_length=50, min_length=5,
#                                 widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    

# class PaymentMethodForm(forms.ModelForm):
#     class Meta:
#         model = PaymentMethod
#         fields = ['card_number', 'expiration_date', 'cvv']
