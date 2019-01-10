from django.db import models

# Create your models here.
class Comment(models.Model):
	patient       = models.ForeignKey(Patient,on_delete=models.CASCADE)
	doctor   	  = models.ForeignKey(Doctor,on_delete=models.CASCADE)
	date          = models.DateField(auto_now_add=True)
	comment       = models.TextField()

	def __str__(self):
		return self.comment

