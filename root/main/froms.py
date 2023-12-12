from django.db import models
from django import forms
from django.forms import ModelForm, TextInput
from .models import JobApplication, User


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['id','full_name', 'phone_number', 'resume']
# Create your models here.


# class registors(ModelForm):
#     class Meta:
#         model = User
#         fields = ['login','password']
#
#         widgets={
#             "login": TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'username'
#             }),
#             "password": TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'password'
#             })
#         }


class loginForm(ModelForm):
    class Meta:
        model = User
        fields = ['login','password']

        widgets={
            "login": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'login'
            }),
            "password": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'password'
            })
        }