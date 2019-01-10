from django.db import models
from patients.models import Patient
from doctors.models import Doctor
from django.utils import timezone

# Create your models here.
class Medicine(models.Model):
	patient        = models.ForeignKey(Patient,on_delete=models.CASCADE)
	refered_by     = models.ForeignKey(Doctor,on_delete=models.CASCADE)
	medicine_name  = models.CharField(max_length=120)
	comment        = models.TextField()
	follow_up_date = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return self.medicine_name


