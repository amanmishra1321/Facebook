from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class CustomerForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('firstname','surname', 'email', 'password','mobile','gender')