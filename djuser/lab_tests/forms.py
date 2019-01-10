from django import forms
from .models import LabTest

class LabTestForm(forms.ModelForm):
	class Meta:
		model= LabTest
		fields=['test_name',]
