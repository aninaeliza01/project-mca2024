from django import forms
from .models import Fuel

class FuelForm(forms.ModelForm):
    class Meta:
        model = Fuel
        fields = ['fueltype', 'price']  # Specify the fields to include in the form

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price
