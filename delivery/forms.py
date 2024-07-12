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

class DeliveryStaffUserForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = DeliveryStaff
        fields = ['is_available', 'phone_number']
        widgets = {
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input' 'ml-5'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        instance = super().save(commit=False)
        user = instance.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            instance.save()
        return instance