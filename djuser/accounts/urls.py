from django.conf.urls import url
from .views import register
from .views import (
    login_view, 
    logout_view, home_view,admin_dashboard,
    edit_admin,delete_user,
    edit_doctor,laboratorist_dashboard,doctor_dashboard,
    medical_dashboard,operator_dashboard,edit_operator,patient_detail,
    register_patient,add_medicine,add_lab_test,edit_medical,doctor_medicine_detail,
    edit_laboratorist,doctor_test_detail,change_password,all_doctor,all_medical,all_laboratorist,
    all_operator,all_patient,doctor_detail,medical_detail,laboratorist_detail,operator_detail,
    doctor_delete,medical_delete,laboratorist_delete,operator_delete,patient_delete
    )


urlpatterns = [
	url(r'^register/$',register, name='register'),
    url(r'^login/$',login_view, name='login'),
    url(r'^logout/$',logout_view, name='logout'),

    url(r'^admin_dashboard/$',admin_dashboard, name='admin_dashboard'),
    url(r'^edit_admin/$',edit_admin, name='edit_admin'),
    url(r'^change_password/$',change_password, name='change_password'),
    url(r'^(?P<pk>\d+)/delete_user/$',delete_user, name='delete_user'),

    url(r'^all_doctor/$',all_doctor, name='all_doctor'),
    url(r'^all_medical/$',all_medical, name='all_medical'),
    url(r'^all_laboratorist/$',all_laboratorist, name='all_laboratorist'),
    url(r'^all_operator/$',all_operator, name='all_operator'),
    url(r'^all_patient/$',all_patient, name='all_patient'),

    url(r'^(?P<id>\d+)/doctor_detail/$',doctor_detail, name='doctor_detail'),
    url(r'^(?P<id>\d+)/medical_detail/$',medical_detail, name='medical_detail'),
    url(r'^(?P<id>\d+)/laboratorist_detail/$',laboratorist_detail, name='laboratorist_detail'),
    url(r'^(?P<id>\d+)/operator_detail/$',operator_detail, name='operator_detail'),
    url(r'^(?P<id>\d+)/patient_detail/$',patient_detail, name='patient_detail'),

    url(r'^(?P<pk>\d+)/doctor_delete/$',doctor_delete, name='doctor_delete'),
    url(r'^(?P<pk>\d+)/medical_delete/$',medical_delete, name='medical_delete'),
    url(r'^(?P<pk>\d+)/laboratorist_delete/$',laboratorist_delete, name='laboratorist_delete'),
    url(r'^(?P<pk>\d+)/operator_delete/$',operator_delete, name='operator_delete'),
    url(r'^(?P<pk>\d+)/patient_delete/$',patient_delete, name='patient_delete'),

    url(r'^doctor_dashboard/$',doctor_dashboard, name='doctor_dashboard'),
    url(r'^edit_doctor/$',edit_doctor, name='edit_doctor'),

    url(r'^(?P<id>\d+)/patient_detail/add_medicine/$',add_medicine, name='add_medicine'),
    url(r'^(?P<id>\d+)/patient_detail/add_lab_test/$',add_lab_test, name='add_lab_test'),

    url(r'^operator_dashboard/$',operator_dashboard, name='operator_dashboard'),
    url(r'^edit_operator/$',edit_operator, name='edit_operator'),
    url(r'^register_patient$',register_patient, name='register_patient'),

    url(r'^medical_dashboard/$',medical_dashboard, name='medical_dashboard'),
    url(r'^edit_medical/$',edit_medical, name='edit_medical'),
    url(r'^(?P<id>\d+)/doctor_medicine_detail/$',doctor_medicine_detail, name='doctor_medicine_detail'),

    url(r'^laboratorist_dashboard/$',laboratorist_dashboard, name='laboratorist_dashboard'),
    url(r'^edit_laboratorist/$',edit_laboratorist, name='edit_laboratorist'),
    url(r'^(?P<id>\d+)/doctor_test_detail/$',doctor_test_detail, name='doctor_test_detail'),
    
] 