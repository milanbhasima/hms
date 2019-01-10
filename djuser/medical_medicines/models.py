from django.db import models
from patients.models import Patient
from medicals.models import Medical
from django.utils import timezone

# Create your models here.
class  MedicalMedicine(models.Model):
	medicine_name=models.CharField(max_length=120)
	comment=models.TextField()
	is_supplied=models.BooleanField(default=False)
	total_amount=models.IntegerField()
	date=models.DateField(default=timezone.now())
	patient= models.ForeignKey(Patient,on_delete=models.CASCADE)
	supplied_by=models.ForeignKey(Medical,on_delete=models.CASCADE)

	def __str__(self):
		return self.medicine_name