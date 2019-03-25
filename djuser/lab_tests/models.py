from django.db import models
from patients.models import Patient
from doctors.models import Doctor
from django.utils import timezone
# Create your models here.
class LabTest(models.Model):
	patient       = models.ForeignKey(Patient,on_delete=models.CASCADE)
	refered_by    = models.ForeignKey(Doctor,on_delete=models.CASCADE)
	test_name     = models.CharField(max_length=120)
	is_sampled	  = models.BooleanField(default=False)
	result        = models.CharField(max_length=120,default='pending',blank=True)
	amount        =models.IntegerField(default=0)
	date          = models.DateField(default=timezone.now())

	def __str__(self):
		return self.test_name
