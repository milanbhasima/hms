from django import forms

class CommentForm(forms.ModelForm):
	class Meta:
		fields=['comment','date']
