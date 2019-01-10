from django import forms
from .models import Admin
from accounts.models import User

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        exclude = ('user',)
        
