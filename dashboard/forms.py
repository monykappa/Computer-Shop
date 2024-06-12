from django import forms
from products.models import *
from django.forms.widgets import FileInput
from django.forms import inlineformset_factory

class MultipleFileInput(FileInput):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        if attrs is None:
            attrs = {}
        attrs.update({'multiple': 'multiple'})
        self.attrs = attrs

class LaptopSpecForm(forms.ModelForm):
    class Meta:
        model = LaptopSpec
        fields = [
            'cpu', 'gpu', 'memory', 'storage', 'display', 'webcam',
            'battery', 'weight', 'operating_system', 'port', 'wireless_connectivity'
        ]
        widgets = {
            'cpu': forms.Select(attrs={'class': 'form-control'}),
            'gpu': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'memory': forms.Select(attrs={'class': 'form-control'}),
            'storage': forms.Select(attrs={'class': 'form-control'}),
            'display': forms.Select(attrs={'class': 'form-control'}),
            'webcam': forms.Select(attrs={'class': 'form-control'}),
            'battery': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.TextInput(attrs={'class': 'form-control'}),
            'operating_system': forms.Select(attrs={'class': 'form-control'}),
            'port': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'wireless_connectivity': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class ProductForm(forms.ModelForm):
    images = forms.FileField(widget=MultipleFileInput(), required=False)

    class Meta:
        model = Product
        exclude = ['slug', 'cpu', 'gpu', 'memory', 'storage', 'display', 'port', 'wireless_connectivity', 'webcam', 'battery', 'operating_system']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        instance = super(ProductForm, self).save(commit=False)
        if commit:
            instance.save()
            images = self.files.getlist('images')
            for image in images:
                ProductImage.objects.create(product=instance, image=image)
        return instance

LaptopSpecFormSet = inlineformset_factory(
    Product, LaptopSpec, form=LaptopSpecForm, extra=1, can_delete=False
)
