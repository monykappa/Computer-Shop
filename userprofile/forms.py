from django import forms
from .models import *

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address1', 'address2', 'city', 'province', 'phone']
        widgets = {
            'address1': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'address2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'province': forms.Select(choices=CAMBODIAN_PROVINCES, attrs={'class': 'form-control', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        required_fields = ['address1', 'city', 'province', 'phone']
        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, 'This field is required.')
        return cleaned_data

