from django import forms
from .models import SocialUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class NewUserForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="",
        widget=(forms.TextInput(attrs={'placeholder':'Email Address'}))
    )
    roll = forms.CharField(
        required=True,
        label="",
        widget=(forms.TextInput(attrs={'placeholder':'Roll'}))
    )
    username = forms.CharField(
        required=True,
        label="",
        widget=(forms.TextInput(attrs={'placeholder':'Username'}))
    )
    password1 = forms.CharField(
        required=True,
        label="",
        widget=(forms.PasswordInput(attrs={'placeholder': 'Password'}))
    )
    password2 = forms.CharField(
        required=True,
        label="",
        widget=(forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    )


    class Meta:
        model = SocialUser
        fields = ('email','roll','username','password1','password2')

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label="",
        widget=(forms.TextInput(attrs={'placeholder':'Enter your Roll or Username'}))
    )
    password = forms.CharField(
        required=True,
        label="",
        widget=(forms.PasswordInput(attrs={'placeholder': 'Enter your Password'}))
    )
    