from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path('patients/', patients_page, name='patients'),
    path('doctors/', doctors_page, name='doctors'),
    path('patients/<int:patient_id>', single_patient, name='patient'),
    path('doctors/<int:doctor_id>', single_doctor, name='doctor'),
    path('add_patient', add_patient, name='add_patient'),
]
