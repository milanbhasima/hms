from django import forms
from .models import Medical

class MedicalForm(forms.ModelForm):
    class Meta:
        model = Medical
        exclude = ('user',)