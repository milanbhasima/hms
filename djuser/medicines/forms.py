from django import forms
from .models import Medicine

class MedicineForm(forms.ModelForm):
	class Meta:
		model = Medicine
		fields=['medicine_name','comment','follow_up_date']
