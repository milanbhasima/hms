from django.contrib.auth import login, logout, get_user_model
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.contrib import messages
from django.db.models import Q
from .forms import UserCreationForm,UserLoginForm,UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

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
from medicines.forms import MedicineForm

from lab_tests.models import LabTest
from lab_tests.forms import LabTestForm

from medical_medicines.models import MedicalMedicine
from medical_medicines.forms import MedicalMedicineForm

from laboratorist_labs.models import LaboratoristLab
from laboratorist_labs.forms import LaboratoristLabForm

User=get_user_model()
# Create your views here.
@login_required(login_url='/accounts/login/')
def register(request, *args, **kwargs):
	if (request.user.is_active and request.user.is_admin):
		form = UserCreationForm(request.POST or None)
		if form.is_valid():
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
		login(request, user_obj)
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
	return render(request,'index.html',{})

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
			'doctor':Doctor.objects.all(),
			'medical':Medical.objects.all(),
			'laboratorist':Laboratorist.objects.all(),
			'operator':Operator.objects.all(),
			'patient':Patient.objects.all(),
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
	instance1=Admin.objects.get(user=instance.id) 
	if form.is_valid():
		form.save()
		# update_session_auth_hash(request,form.user)
		messages.success(request,'Congratulation! you have successfully updated password')
		return redirect('admin_dashboard')
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
	context_dict={
		'patient':instance,
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
		}
	return render(request,'doctor_form.html',context_dict)

# @login_required(login_url='/accounts/login/')
# def patient_detail(request,id=None):
# 	if not request.user.is_doctor:
# 		raise Http404
# 	instance=get_object_or_404(Patient,id=id)
# 	context_dict={
# 		'patient':instance,
# 	}
# 	return render(request,'patient_detail.html', context_dict)

@login_required(login_url='/accounts/login/')
def add_medicine(request,id=None):
	if not request.user.is_doctor:
		raise Http404
	form=MedicineForm(request.POST or None)
	instance=get_object_or_404(Patient,id=id)
	# instance1=get_object_or_404(User,id=request.user.id)
	# instance2=get_object_or_404(Doctor,user=instance1.id)
	# instance1=User.objects.get(id=request.user.id)
	# instance2=Doctor.objects.get(user=instance1.id)
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
		return redirect('doctor_dashboard')
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
		labTest.save()
		return redirect('doctor_dashboard')
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
	uform=UserCreationForm(request.POST or None, request.FILES or None, instance=instance)
	oform=OperatorForm(request.POST or None , request.FILES or None, instance=instance1)
	context_dict={                       
		'uform':uform,
		'oform':oform,
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
	instance1=Medicine.objects.filter(patient_id=instance.id).order_by('-follow_up_date')
	form=MedicalMedicineForm(request.POST or None)
	context_dict={
		'patient':instance,
		'doctor':instance1,
		'form':form,
	}
	if form.is_valid():
		medical_medicine = form.save(commit=False)
		login_user_id=request.user.id
		instance1=Medical.objects.get(user_id=login_user_id) 
		medical_medicine.supplied_by=instance1
		medical_medicine.patient_id=instance.id
		medical_medicine.save()
		return redirect('medical_dashboard')
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
	form=LaboratoristLabForm(request.POST or None)
	context_dict={
		'patient':instance,
		'doctor':instance1,
		'form':form,
	}
	if form.is_valid():
		lab = form.save(commit=False)
		login_user_id=request.user.id
		instance1=Laboratorist.objects.get(user_id=login_user_id) 
		lab.test_by=instance1
		lab.patient_id=instance.id
		lab.save()
		return redirect('laboratorist_dashboard')
	return render(request,'doctor_test_detail.html', context_dict)
