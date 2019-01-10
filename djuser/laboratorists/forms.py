from django import forms
from .models import Laboratorist

class LaboratoristForm(forms.ModelForm):
    class Meta:
        model = Laboratorist
        exclude = ('user',)
