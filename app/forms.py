from django import forms
from .models import Product,Category
from django.contrib.auth.models import User
from .models import Profile

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



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'id': 'file-upload',      # give it ID
                'style': 'display:none;'  # hide it
            })
        }
