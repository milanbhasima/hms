from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from django.shortcuts import render,get_object_or_404
from .utils import render_to_pdf
from patients.models import Patient
from medicines.models import Medicine
from .forms import ContactForm

# class GeneratePDF(View):
# 	def get(self, request, *args, **kwargs):
# 		template=get_template('medicine_bill.html')
# 		instance=get_object_or_404(Patient,id=id)
# 		medicine_list=Medicine.objects.filter(patient_id=instance.id)
# 		total_prices = sum(medicine.amount for medicine in medicine_list)
# 		context={
# 			'patient':instance,
# 			'dm':medicine_list,
# 			'total_prices':total_prices,
# 		}
# 		html = template.render(context)
# 		return HttpResponse(html)



def pdf(request,id):
		template=get_template('medicine_bill.html')
		instance=get_object_or_404(Patient,id=id)
		medicine_list=Medicine.objects.filter(patient_id=instance.id)
		total_prices = sum(medicine.amount for medicine in medicine_list)
		context={
			'patient':instance,
			'dm':medicine_list,
			'total_prices':total_prices,
		}
		html = template.render(context)
		pdf = render_to_pdf('medicine_bill.html',context)
		if pdf:
			return HttpResponse(pdf, content_type='application/pdf')
		return HttpResponse("Not Found")
