from django import forms
from django.forms import ModelForm
from .models import Venue

class registerForm(ModelForm):
    class Meta:
        model=User
        fields=""
    