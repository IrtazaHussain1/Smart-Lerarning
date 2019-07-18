from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from Login_app.choices import *
from django.core import validators
from Login_app.models import Teacher


class UserRegisterForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}),label='Password')
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}),label='Confirm Password')
    class Meta:
        model= User
        fields= ('username','first_name','last_name','email',    'password1', 'password2',)
        widgets={
        'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'First Name'}),
        'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Last Name'}),
        'username': forms.TextInput(attrs={'class': 'form-control','placeholder':'Username'}),
        'email': forms.TextInput(attrs={'class': 'form-control','placeholder':'Email'}),
        }
class Profile(forms.ModelForm):
    class Meta:
        model= Teacher
        exclude=['t_teacher']
        labels= {'t_gender':'Gender','t_departmant':'Department'}
        widgets={
        't_gender': forms.Select(choices="gender_list",attrs={'class': 'form-control'}),
        't_departmant': forms.Select(choices="department_list",attrs={'class': 'form-control'}),
        }
