from django.contrib.auth import login, logout, get_user_model
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.contrib import messages
from django.db.models import Q
from .forms import UserCreationForm,UserLoginForm,UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from djuser.utils import render_to_pdf
from djuser.forms import ContactForm
from django.conf import settings
from django.core.mail import send_mail
from datetime import date

from accounts.models import User

from admins.models import Admin
from admins.forms import AdminForm

from doctors.models import Doctor
from doctors.forms import DoctorForm

from medicals.models import Medical
from medicals.forms import MedicalForm

from operators.models import Operator
from operators.forms import OperatorForm

from laboratorists.models import Laboratorist
from laboratorists.forms import LaboratoristForm

from patients.models import Patient
from patients.forms import PatientForm

from medicines.models import Medicine
from medicines.forms import MedicineForm,MedicinesForm

from lab_tests.models import LabTest
from lab_tests.forms import LabTestForm

User=get_user_model()
# Create your views here.
@login_required(login_url='/accounts/login/')
def register(request, *args, **kwargs):
	if (request.user.is_active and request.user.is_admin):
		form = UserCreationForm(request.POST or None)
		if form.is_valid():
			name=form.cleaned_data.get('name')
			email=form.cleaned_data.get('email')
			password=form.cleaned_data.get('password')
			subject='User Password'
			from_email=settings.EMAIL_HOST_USER
			to_email= email
			your_message="%s : Your Password is (%s) via %s"%(name, password, email)
			send_mail(
				subject,
				your_message,
				from_email,
				[to_email,],
				fail_silently=False
				)
			form.save()
			
			latest_id=User.objects.latest('id')

			if(form.cleaned_data.get('is_doctor')==True):
				doctor=Doctor(user=latest_id)
				doctor.save()

			elif(form.cleaned_data.get('is_medical')==True):
				medical=Medical(user=latest_id)
				medical.save()

			elif(form.cleaned_data.get('is_laboratorist')==True):
				laboratorist=Laboratorist(user=latest_id)
				laboratorist.save()

			elif(form.cleaned_data.get('is_operator')==True):
				operator=Operator(user=latest_id)
				operator.save()

			elif(form.cleaned_data.get('is_admin')==True):
				admin=Admin(user=latest_id)
				admin.save()


			print('user created succefully')
			messages.success(request,'Congratulation! you have successfully registered staff')
			return HttpResponseRedirect('/accounts/login')
	else:
		return HttpResponse('<h1>Sorry only staff and admin can register here</h1>')
	return render(request,'register.html',{'form':form})


def login_view(request, *args, **kwargs):
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		user_obj = User.objects.get(email__iexact = form.cleaned_data.get('email'))
		login(request, user_obj, backend='django.contrib.auth.backends.ModelBackend')
		if request.user.is_doctor:
			return redirect("doctor_dashboard")
		elif request.user.is_medical:
			return redirect('medical_dashboard')
		elif request.user.is_laboratorist:
			return redirect('laboratorist_dashboard')
		elif request.user.is_admin:
			return redirect('admin_dashboard')
		elif request.user.is_operator:
			return redirect('operator_dashboard')
		else:
			return redirect('home')
	return render(request,'login.html',{'form':form})

@login_required(login_url='/accounts/login/')
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def home_view(request):
	form=ContactForm(request.POST or None)
	if form.is_valid():
		# for key,value in form.cleaned_data.items():
		# 	print (key,value)
		name=form.cleaned_data.get('name')
		email=form.cleaned_data.get('email')
		contact=form.cleaned_data.get('contact')
		comment=form.cleaned_data.get('comment')
		subject='contact form'
		from_email=settings.EMAIL_HOST_USER
		to_email= from_email
		contact_message="%s : %s via %s"%(name, comment, email)
		send_mail(
			subject,
			contact_message,
			from_email,
			[to_email,],
			fail_silently=False
			)
	context={
		'form':form,
	}
	return render(request,'index.html',context)

@login_required(login_url='/accounts/login/')
def admin_dashboard(request):
	if request.user.is_admin:
		queryset=User.objects.all()
		query=request.GET.get('q')
		if query:
			queryset=queryset.filter(
				Q(id__iexact=query)
				).distinct()
		context_dict={
			'doctor':Doctor.objects.all()[:2],
			'medical':Medical.objects.all()[:2],
			'laboratorist':Laboratorist.objects.all()[:2],
			'operator':Operator.objects.all()[:2],
			'patient':Patient.objects.all()[:2],
			'instance':Admin.objects.get(user_id=request.user.id),
		}
		return render(request,'admin_dashboard.html',context_dict)
	else:
		raise Http404

@login_required(login_url='/accounts/login/')
def edit_admin(request):
	if not request.user.is_admin:
		raise Http404
	instance=User.objects.get(id=request.user.id)
	instance1=Admin.objects.get(user=instance.id) 
	uform=UserChangeForm(request.POST or None, request.FILES or None, instance=instance)
	aform=AdminForm(request.POST or None , request.FILES or None, instance=instance1)
	context_dict={                       
		'uform':uform,
		'aform':aform,
		'instance':instance1,
		}
	if uform.is_valid() and aform.is_valid():
		uform.save()
		aform.save()
		messages.success(request,'Congratulation! you have successfully updated %s profile' %(request.user.name))
		return redirect('admin_dashboard')
	return render(request,'admin_form.html',context_dict)

@login_required(login_url='/accounts/login/')
def change_password(request):
	if not request.user.is_authenticated:
		raise Http404
	form=PasswordChangeForm(data=request.POST or None,user=request.user)
	instance=User.objects.get(id=request.user.id)
	if request.user.is_admin:
		instance1=Admin.objects.get(user=instance.id) 
	elif request.user.is_doctor:
		instance1=Doctor.objects.get(user=instance.id)
	elif request.user.is_medical:
		instance1=Medical.objects.get(user=instance.id)
	elif request.user.is_operator:
		instance1=Operator.objects.get(user=instance.id)
	elif request.user.is_laboratorist:
		instance1=Laboratorist.objects.get(user=instance.id) 
	if form.is_valid():
		form.save()
		# update_session_auth_hash(request,form.user)
		messages.success(request,'Congratulation! you have successfully updated password')
		if request.user.is_admin:
			return redirect('admin_dashboard')
		elif request.user.is_doctor:
			return redirect('doctor_dashboard')
		elif request.user.is_medical:
			return redirect('medical_dashboard')
		elif request.user.is_operator:
			return redirect('operator_dashboard')
		elif request.user.is_laboratorist:
			return redirect('laboratorist_dashboard')
	context_dict={                       
		'form':form,
		'instance':instance1,
		}
	return render(request,'change_password.html',context_dict)


@login_required(login_url='/accounts/login/')
def all_doctor(request):
	queryset=Doctor.objects.all()
	context_dict={
		'doctor':queryset,
	}
	return render(request,'all_doctor.html',context_dict)

@login_required(login_url='/accounts/login/')
def all_medical(request):
	queryset=Medical.objects.all()
	context_dict={
		'medical':queryset,
	}
	return render(request,'all_medical.html',context_dict)

@login_required(login_url='/accounts/login/')
def all_laboratorist(request):
	queryset=Laboratorist.objects.all()
	context_dict={
		'laboratorist':queryset,
	}
	return render(request,'all_laboratorist.html',context_dict)

@login_required(login_url='/accounts/login/')
def all_operator(request):
	queryset=Operator.objects.all()
	context_dict={
		'operator':queryset,
	}
	return render(request,'all_operator.html',context_dict)

@login_required(login_url='/accounts/login/')
def all_patient(request):
	queryset=Patient.objects.all()
	context_dict={
		'patient':queryset,
	}
	return render(request,'all_patient.html',context_dict)

@login_required(login_url='/accounts/login/')
def doctor_detail(request,id=None):
	if not request.user.is_admin:
		raise Http404
	instance=Doctor.objects.get(id=id)
	context_dict={
		'doctor':instance,
	}
	return render(request,'doctor_detail.html', context_dict)

@login_required(login_url='/accounts/login/')
def medical_detail(request,id=None):
	if not request.user.is_admin:
		raise Http404
	instance=Medical.objects.get(id=id)
	context_dict={
		'medical':instance,
	}
	return render(request,'medical_detail.html', context_dict)

@login_required(login_url='/accounts/login/')
def laboratorist_detail(request,id=None):
	if not request.user.is_admin:
		raise Http404
	instance=Laboratorist.objects.get(id=id)
	context_dict={
		'laboratorist':instance,
	}
	return render(request,'laboratorist_detail.html', context_dict)

@login_required(login_url='/accounts/login/')
def operator_detail(request,id=None):
	if not request.user.is_admin:
		raise Http404
	instance=Operator.objects.get(id=id)
	context_dict={
		'operator':instance,
	}
	return render(request,'operator_detail.html', context_dict)
	

@login_required(login_url='/accounts/login/')
def patient_detail(request,id=None):
	# if not request.user.is_admin:
	# 	raise Http404
	instance=Patient.objects.get(id=id)
	instance1=Medicine.objects.filter(patient_id=instance.id).order_by('-date')
	instance2=LabTest.objects.filter(patient_id=instance.id).order_by('date')
	# form=MedicinesForm(request.POST or None)
	context_dict={
		'patient':instance,
		'doctor':instance1,
		'doctors':instance2,
		# 'form':form,
	}
	return render(request,'patient_detail.html', context_dict)


@login_required(login_url='/accounts/login/')
def delete_user(request,pk=None):
	if not request.user.is_admin:
		raise Http404
	instance=get_object_or_404(User,id=pk)
	instance.delete()
	messages.success(request,'User deleted')
	return redirect('admin_dashboard')

@login_required(login_url='/accounts/login/')
def doctor_delete(request,pk=None):
	if not request.user.is_admin:
		raise Http404
	instance=get_object_or_404(User,id=pk)
	instance.delete()
	messages.success(request,'Doctor deleted')
	return redirect('admin_dashboard')

@login_required(login_url='/accounts/login/')
def medical_delete(request,pk=None):
	if not request.user.is_admin:
		raise Http404
	instance=get_object_or_404(User,id=pk)
	instance.delete()
	messages.success(request,'Medical deleted')
	return redirect('admin_dashboard')

@login_required(login_url='/accounts/login/')
def laboratorist_delete(request,pk=None):
	if not request.user.is_admin:
		raise Http404
	instance=get_object_or_404(User,id=pk)
	instance.delete()
	messages.success(request,'Laboratorist deleted')
	return redirect('admin_dashboard')

@login_required(login_url='/accounts/login/')
def operator_delete(request,pk=None):
	if not request.user.is_admin:
		raise Http404
	instance=get_object_or_404(User,id=pk)
	instance.delete()
	messages.success(request,'Operator deleted')
	return redirect('admin_dashboard')

@login_required(login_url='/accounts/login/')
def patient_delete(request,pk=None):
	if not request.user.is_admin:
		raise Http404
	instance=get_object_or_404(Patient,id=pk)
	instance.delete()
	messages.success(request,'Patient deleted')
	return redirect('admin_dashboard')


@login_required(login_url='/accounts/login/')
def doctor_dashboard(request):
	if request.user.is_doctor:
		queryset=Patient.objects.all()
		query=request.GET.get('q')
		if query:
			queryset=queryset.filter(
				Q(id__iexact=query)
				).distinct()
		context_dict={
			'patient_list':queryset,
			'instance':Doctor.objects.get(user_id=request.user.id),
		}
		return render(request,'doctor_dashboard.html',context_dict)
	else:
		raise Http404


@login_required(login_url='/accounts/login/')
def edit_doctor(request):
	if not request.user.is_doctor:
		raise Http404
	instance=User.objects.get(id=request.user.id)
	instance1=Doctor.objects.get(user=instance.id) 
	uform=UserChangeForm(request.POST or None, request.FILES or None, instance=instance)
	dform=DoctorForm(request.POST or None , request.FILES or None, instance=instance1)
	if uform.is_valid() and dform.is_valid():
		uform.save()
		dform.save()
		messages.success(request,'Congratulation! you have successfully updated %s profile' %(request.user.name))
		return redirect('doctor_dashboard')
	context_dict={                       
		'uform':uform,
		'dform':dform,
		'instance':Doctor.objects.get(user_id=request.user.id),
		}
	return render(request,'doctor_form.html',context_dict)


@login_required(login_url='/accounts/login/')
def add_medicine(request,id=None):
	if not request.user.is_doctor:
		raise Http404
	form=MedicineForm(request.POST or None)
	instance=get_object_or_404(Patient,id=id)
	context_dict={
		'form':form,
		'patient':instance,
	}
	if form.is_valid():
		medicine = form.save(commit=False)
		login_user_id=request.user.id
		instance1=Doctor.objects.get(user_id=login_user_id)
		medicine.refered_by=instance1
		medicine.patient_id=instance.id
		medicine.save()
		return redirect('patient_detail',id=id) 
	return render(request,'medicine_form.html',context_dict)

@login_required(login_url='/accounts/login/')
def add_lab_test(request,id=None):
	if not request.user.is_doctor:
		raise Http404
	form=LabTestForm(request.POST or None)
	instance=get_object_or_404(Patient,id=id)
	instance1=User.objects.get(id=request.user.id)
	instance2=Doctor.objects.get(user=instance1.id)
	context_dict={
		'form':form,
		'patient':instance,
	}
	if form.is_valid():
		labtest = form.save(commit=False)
		labtest.patient_id=instance.id
		labtest.refered_by_id=instance2.id
		labtest.save()
		return redirect('patient_detail',id=id)
	return render(request,'lab_test_form.html',context_dict)

@login_required(login_url='/accounts/login/')
def operator_dashboard(request):
	if request.user.is_operator:
		context_dict={
			'patient_list':Patient.objects.all(),
			'instance':Operator.objects.get(user_id=request.user.id),
		}
		return render(request,'operator_dashboard.html',context_dict)
	else:
		raise Http404
		

@login_required(login_url='/accounts/login/')
def edit_operator(request):
	if not request.user.is_operator:
		raise Http404
	instance=User.objects.get(id=request.user.id)
	instance1=Operator.objects.get(user_id=instance.id) 
	uform=UserChangeForm(request.POST or None, request.FILES or None, instance=instance)
	oform=OperatorForm(request.POST or None , request.FILES or None, instance=instance1)
	context_dict={                       
		'uform':uform,
		'oform':oform,
		'instance':Operator.objects.get(user_id=request.user.id),
		}
	if uform.is_valid() and oform.is_valid():
		uform.save()
		oform.save()	
		messages.success(request,'Congratulation! you have successfully updated %s profile' %(request.user.name))
		return redirect('operator_dashboard')
	return render(request,'operator_form.html',context_dict)

@login_required(login_url='/accounts/login/')
def register_patient(request):
	if not request.user.is_operator:
		raise Http404
	form=PatientForm(request.POST or None)
	context_dict={
		'form':form,
		'instance':Operator.objects.get(user_id=request.user.id),
		}
	if form.is_valid():
		form.save()
		return redirect('operator_dashboard')
	return render(request,'register_patient.html',context_dict)


@login_required(login_url='/accounts/login/')
def medical_dashboard(request):
	if request.user.is_medical:
		queryset=Patient.objects.all()
		query=request.GET.get('q')
		if query:
			queryset=queryset.filter(
				Q(id__iexact=query)
				).distinct()
		context_dict={
			'patient_list':queryset,
			'instance':Medical.objects.get(user_id=request.user.id),
		}
		return render(request,'medical_dashboard.html',context_dict)
	else:
		raise Http404

@login_required(login_url='/accounts/login/')
def edit_medical(request):
	if not request.user.is_medical:
		raise Http404
	instance=User.objects.get(id=request.user.id)
	instance1=Medical.objects.get(user_id=instance.id) 
	uform=UserChangeForm(request.POST or None, request.FILES or None, instance=instance)
	mform=MedicalForm(request.POST or None , request.FILES or None, instance=instance1)
	if uform.is_valid() and mform.is_valid():
		uform.save()
		mform.save()
		messages.success(request,'Congratulation! you have successfully updated %s profile' %(request.user.name))
		return redirect('medical_dashboard')
	context_dict={                       
		'uform':uform,
		'mform':mform,
		'instance':Medical.objects.get(user_id=request.user.id),
		} 
	return render(request,'medical_form.html',context_dict)

@login_required(login_url='/accounts/login/')
def doctor_medicine_detail(request,id=None):
	if not request.user.is_medical:
		raise Http404
	instance=get_object_or_404(Patient,id=id)
	form=MedicinesForm(request.POST or None)
	instance1=Medicine.objects.filter(patient_id=instance.id).filter(date=date.today())
	medical=Medical.objects.get(user_id=request.user.id)
	context_dict={
		'patient':instance,
		'dm':instance1,
		'form':form,
	}
	if request.POST.get('id') is not None:
		a=Medicine.objects.get(id=request.POST.get('id'))
		a.is_purchased=True
		a.amount=request.POST.get('amount')
		a.supplied_by_id=medical.id
		a.purchase_now=request.POST.get("purchase_now")
		print("Purchase_now:",a.purchase_now)
		if a.purchase_now=='on':
			a.purchase_now=True
		else:
			a.purchase_now=False
		a.save()
		return redirect('doctor_medicine_detail',id=id)
	return render(request,'doctor_medicine_detail.html', context_dict)

@login_required(login_url='/accounts/login/')
def laboratorist_dashboard(request):
	if request.user.is_laboratorist:
		queryset=Patient.objects.all()
		query=request.GET.get('q')
		if query:
			queryset=queryset.filter(
				Q(id__iexact=query)
				).distinct()
		context_dict={
			'patient_list':queryset,
			'instance':Laboratorist.objects.get(user_id=request.user.id),
		}
		return render(request,'laboratorist_dashboard.html',context_dict)
	else:
		raise Http404

@login_required(login_url='/accounts/login/')
def edit_laboratorist(request):
	if not request.user.is_laboratorist:
		raise Http404
	instance=User.objects.get(id=request.user.id)
	instance1=Laboratorist.objects.get(user_id=instance.id) 
	uform=UserChangeForm(request.POST or None, request.FILES or None, instance=instance)
	lform=LaboratoristForm(request.POST or None , request.FILES or None, instance=instance1)
	if uform.is_valid() and lform.is_valid():
		uform.save()
		lform.save()
		messages.success(request,'Congratulation! you have successfully updated %s profile' %(request.user.name))
		return redirect('laboratorist_dashboard')
	context_dict={                       
		'uform':uform,
		'lform':lform,
		} 
	return render(request,'laboratorist_form.html',context_dict)

@login_required(login_url='/accounts/login/')
def doctor_test_detail(request,id=None):
	if not request.user.is_laboratorist:
		raise Http404
	instance=get_object_or_404(Patient,id=id)
	instance1=LabTest.objects.filter(patient_id=instance.id)
	context_dict={
		'patient':instance,
		'dt':instance1,
	}
	if request.POST.get('id') is not None:
		a=LabTest.objects.get(id=request.POST.get('id'))
		a.is_sampled=True
		a.result=request.POST.get('result')
		a.amount=request.POST.get('amount')
		a.save()
		return redirect('doctor_test_detail',id=id)
	return render(request,'doctor_test_detail.html', context_dict)

@login_required(login_url='/accounts/login/')
def lab_bill(request,id=None):
	if not request.user.is_laboratorist:
		raise Http404 
	instance=get_object_or_404(Patient,id=id)
	instance1=LabTest.objects.filter(patient_id=instance.id)
	total_prices = sum(test.amount for test in instance1)
	context_dict={
		'patient':instance,
		'dt':instance1,
		'total_prices':total_prices,
	}
	return render(request,'lab_bill.html', context_dict)

@login_required(login_url='/accounts/login/')
def medicine_bill(request,id=None):
	if not request.user.is_medical:
		raise Http404 
	instance=get_object_or_404(Patient,id=id)
	medicine_list=Medicine.objects.filter(patient_id=instance.id).filter(date=date.today()).filter(purchase_now=True)
	total_prices = sum(medicine.amount for medicine in medicine_list)
	context={
		'patient':instance,
		'dm':medicine_list,
		'total_prices':total_prices,
	}
	# return render(request,'medicine_bill.html', context_dict)
	# html = template.render(context)
	# return HttpResponse(html)
	pdf=render_to_pdf('medicine_bill.html',context)
	return HttpResponse(pdf,content_type='application/pdf') 


def check_patient(request):
	if not request.user.is_doctor:
		raise Http404
	# instance=get_object_or_404(Patient,id=id)
	doc=Doctor.objects.get(user_id=request.user.id)
	patient=Medicine.objects.filter(refered_by_id=doc.id)
	context={
		'patient':patient,
	}
	return render(request,'check_patient.html',context)

def patient_report(request): 
	queryset=Patient.objects.all()
	query=request.GET.get('q')
	if query:
		queryset=queryset.filter(
			Q(id__iexact=query)
			).distinct()
		instance=get_object_or_404(Patient,id=query)
		medicine_list=Medicine.objects.filter(patient_id=instance.id)
		total_prices = sum(medicine.amount for medicine in medicine_list)
		context={
		'patient':instance,
		'dm':medicine_list,
		'total_prices':total_prices,
		}
		pdf=render_to_pdf('medicine_bill.html',context)
		return HttpResponse(pdf,content_type='application/pdf')
	context_dict={
		'report':'No report to show'
	}
	return render(request,'patient_form.html',context_dict)
