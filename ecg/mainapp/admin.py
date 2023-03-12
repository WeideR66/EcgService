from django.contrib import admin
from .models import EcgData, Doctor, Patient

# Register your models here.
class EcgDataInLine(admin.TabularInline):
    model = EcgData


class PatientAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient_name', 'patient_surname', 'date_time', 'doctor_id']
    inlines = (EcgDataInLine,)


class DoctorAdmin(admin.ModelAdmin):
   list_display = ['id', 'doctor_name', 'doctor_surname', 'job_title']


admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)