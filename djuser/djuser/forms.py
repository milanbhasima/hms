from django import forms

class ContactForm(forms.Form):
	name= forms.CharField()
	contact=forms.IntegerField()
	email=forms.EmailField()
	comment=forms.CharField()
