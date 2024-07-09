# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import DeliveryStaff
from orders.models import *



class DeliveryStaffCreationForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label='Phone Number', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))  

    class Meta:
        model = DeliveryStaff
        fields = ['username', 'email', 'password', 'phone_number', 'is_available']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        delivery_staff = super().save(commit=False)
        delivery_staff.user = user
        delivery_staff.phone_number = self.cleaned_data['phone_number']  
        if commit:
            delivery_staff.save()
        return delivery_staff


class AssignOrderForm(forms.Form):
    orders = forms.ModelMultipleChoiceField(
        queryset=OrderHistory.objects.filter(status='Pending', delivery_assignment__isnull=True),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    delivery_staff = forms.ModelChoiceField(
        queryset=DeliveryStaff.objects.filter(is_available=True),
        empty_label="Select a delivery staff",
        widget=forms.Select(attrs={'class': 'form-select'})
    )