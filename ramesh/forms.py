from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["first_name","last_name","username", "email", "password1", "password2"]


        widgets = {
    'first_name': forms.TextInput(attrs={'class':'form-control'}),
    'last_name': forms.TextInput(attrs={'class':'form-control'}),
    'username': forms.TextInput(attrs={'class':'form-control'}),
    'email': forms.EmailInput(attrs={'class':'form-control'}),
    'password1': forms.PasswordInput(attrs={'class':'form-control'}),
    'password2': forms.PasswordInput(attrs={'class':'form-control'}),
}