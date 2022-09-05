from tkinter import Widget
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .models import Customer, Userprofile


class LoginUser(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control;', 'placeholder': 'Password'}))

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "First name"}))
    last_name = forms.CharField(label="", widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Last name"}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Username"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}))
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "First Name*"
        self.fields['last_name'].label = "Last Name*"


        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            print("here")
            raise forms.ValidationError(u'Username "%s" is already in use.' % username)
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            print("here")
            raise forms.ValidationError(u'Email "%s" is already in use.' % email)
        return email


class UserprofileForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['image']



class CustomerForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Name'}))
    table_number = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control;', 'placeholder': 'Table Number'}))
    class Meta:
        model = Customer
        fields = ['name', 'table_number']