from django.shortcuts import render
from .forms import DoctorForm
# Create your views here.
def create_doctor(request):
	form=DoctorForm(request.POST or None)
	template_name='doctor_form.html'
	context_dict={
		'form':form,
	}
	return render(request,template_name,context_dict)