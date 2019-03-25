from django import forms
from .models import LabTest

class LabTestForm(forms.ModelForm):
	class Meta:
		model= LabTest
		fields=['date', 'test_name']


class LabTestsForm(forms.ModelForm):
	class Meta:
		model= LabTest
		fields=['date', 'test_name', 'result','amount','is_sampled']