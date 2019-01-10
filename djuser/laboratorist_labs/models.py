from django.db import models
from patients.models import Patient
from laboratorists.models import Laboratorist
from django.utils import timezone

# Create your models here.
class LaboratoristLab(models.Model):
	test_name=models.CharField(max_length=120)
	test_level=models.CharField(max_length=120)
	comment=models.TextField()
	is_done=models.BooleanField(default=False)
	test_date=models.DateField(default=timezone.now())
	patient= models.ForeignKey(Patient,on_delete=models.CASCADE)
	test_by=models.ForeignKey(Laboratorist,on_delete=models.CASCADE)

	def __str__(self):
		return self.test_name