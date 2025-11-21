from django import forms
from .models import Product,Category
from django.contrib.auth.models import User


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description','category', 'image']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-field'}),
            'price': forms.NumberInput(attrs={'class': 'input-field'}),
            'description': forms.Textarea(attrs={'class': 'input-field'}),
            'category':forms.TextInput(attrs={'class':'input-field'}),
            'image': forms.FileInput(attrs={'class': 'input-field'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields =['name', 'description']





   
