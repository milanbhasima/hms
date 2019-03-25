from django import forms
from .models import Medicine

class MedicineForm(forms.ModelForm):
	follow_up_date = forms.DateField(widget = forms.SelectDateWidget)
	class Meta:
		model = Medicine
		fields=['date','medicine_name','comment','follow_up_date']

class MedicinesForm(forms.ModelForm):
	follow_up_date = forms.DateField(widget = forms.SelectDateWidget)
	class Meta:
		model = Medicine
		fields=['date','medicine_name','comment','follow_up_date','is_purchased','purchase_now','amount']