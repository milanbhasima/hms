from django import forms
from .models import LaboratoristLab

class LaboratoristLabForm(forms.ModelForm):
	class Meta:
		model = LaboratoristLab
		fields=['test_name','test_level','comment','is_done','test_date']