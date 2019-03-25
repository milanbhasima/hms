from django.db import models
from patients.models import Patient
from medicals.models import Medical
from doctors.models import Doctor
from django.utils import timezone

# Create your models here.
class Medicine(models.Model):
	patient        = models.ForeignKey(Patient,on_delete=models.CASCADE)
	refered_by     = models.ForeignKey(Doctor,on_delete=models.CASCADE)
	supplied_by    = models.ForeignKey(Medical,on_delete=models.CASCADE,blank=True,null=True)
	medicine_name  = models.CharField(max_length=120)
	comment        = models.TextField()
	follow_up_date = models.DateTimeField(blank=True, null=True)
	is_purchased   = models.BooleanField(default=False)
	purchase_now   = models.BooleanField(default=False)
	amount         = models.IntegerField(default=0)
	date           = models.DateField(default=timezone.now())

	def __str__(self):
		return self.medicine_name

