from django import forms
from .models import Fuel

class FuelForm(forms.ModelForm):
    class Meta:
        model = Fuel
        fields = ['fueltype', 'price']  # Specify the fields to include in the form
