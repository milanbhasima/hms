from django.conf.urls import url
from .views import create_doctor
urlpatterns = [
	url(r'^create_doctor/$',create_doctor, name='create_doctor'),
]