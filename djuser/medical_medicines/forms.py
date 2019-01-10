from django import forms
from .models import MedicalMedicine

class MedicalMedicineForm(forms.ModelForm):
	class Meta:
		model = MedicalMedicine
		fields=['medicine_name','comment','is_supplied','date','total_amount']