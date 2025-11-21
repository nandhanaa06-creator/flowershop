
from django import forms
from django.contrib.auth.models import User
from account.models import Profile


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