from django import forms
from .models import LaptopPriceAlert

class LaptopPriceAlertForm(forms.ModelForm):
    class Meta:
        model = LaptopPriceAlert
        fields = ['laptop_name', 'desired_price']
