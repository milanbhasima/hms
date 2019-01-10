# Create your models here.
from django.db import models
from django.utils import timezone
from accounts.models import User

# Create your models here.
class Patient(models.Model):
	name= models.CharField(max_length=120)	
	age = models.PositiveIntegerField(default=0)
	address=models.CharField(max_length=120)
	sex=models.CharField(max_length=120,choices=(('Male','Male'),('Female','Female')),default="Male")
	contact = models.CharField(max_length=120)
	date = models.DateField(auto_now_add=True)
	description = models.TextField(null=False, blank=False)

	def __str__(self):
		return self.name