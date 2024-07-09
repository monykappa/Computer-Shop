# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import DeliveryStaff
from orders.models import *

class DeliveryStaffCreationForm(forms.ModelForm):
    username = forms.CharField(label='Username')
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = DeliveryStaff
        fields = ['username', 'email', 'password', 'is_available']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        delivery_staff = super().save(commit=False)
        delivery_staff.user = user
        if commit:
            delivery_staff.save()
        return delivery_staff


class AssignOrderForm(forms.Form):
    orders = forms.ModelMultipleChoiceField(
        queryset=OrderHistory.objects.filter(status='Pending', delivery_assignment__isnull=True),
        widget=forms.CheckboxSelectMultiple
    )
    delivery_staff = forms.ModelChoiceField(
        queryset=DeliveryStaff.objects.filter(is_available=True),
        empty_label="Select a delivery staff"
    )