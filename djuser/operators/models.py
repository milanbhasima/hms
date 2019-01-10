from django.db import models
from django.utils import timezone
from accounts.models import User

# Create your models here.
class Operator(models.Model):
	user=models.OneToOneField(User)
	contact = models.CharField(max_length=120)
	age = models.PositiveIntegerField(default=0)
	permanent_address=models.CharField(max_length=120)
	temporary_address=models.CharField(max_length=120)
	qualification = models.CharField(max_length=120)
	degree = models.CharField(max_length=120)
	image= models.FileField(upload_to='profile',blank=True,null=True)
	joined_date = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.user.name
