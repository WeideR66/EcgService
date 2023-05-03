from django.shortcuts import render, redirect
from .models import Doctor, Patient, EcgData
from .forms import PatientCreationForm, UserAuthForm
from django.contrib.auth import login, logout


def login_user(request):
    if request.method == 'POST':
        data = UserAuthForm(data=request.POST)
        if data.is_valid():
            login(request, data.get_user())
            return redirect('home')
    else:
        data = UserAuthForm()
    return render(request,
                  template_name='index.html',
                  context={'dat': data})


def logout_user(request):
    logout(request)
    return redirect('login_user')


def home_page(request):
    return render(request,
                  template_name='main_page.html')


def patients_page(request):
    all_patients = Patient.objects.all()
    return render(request,
                  template_name='patients_page.html',
                  context={'patients': all_patients})


def doctors_page(request):
    all_doctors = Doctor.objects.all()
    return render(request,
                  template_name='doctors_page.html',
                  context={'doctors': all_doctors})


def single_patient(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    return render(request,
                  template_name='single_patient.html',
                  context={'data': patient})


def single_doctor(request, doctor_id):
    doc_patients = Patient.objects.filter(doctor_id=doctor_id)
    return render(request,
                  template_name='single_doctor.html',
                  context={'doc': doc_patients[0],
                           'patients': doc_patients})


def add_patient(request):
    if request.method == 'POST':
        data = PatientCreationForm(request.POST, files=request.FILES)
        if data.is_valid():
            hea_file, dat_file = None, None
            for file in request.FILES.getlist('files'):
                if file.name.endswith('.hea'):
                    hea_file = file
                else:
                    dat_file = file
            req_data = request.POST
            doctor = Doctor.objects.get(pk=req_data['doctor'])
            patient = Patient(
                doctor=doctor,
                patient_name=req_data['name'],
                patient_surname=req_data['surname'],
            )
            patient.save()
            data = EcgData(
                patient=patient,
                ecg_hea_file=hea_file,
                ecg_dat_file=dat_file
            )
            data.save()
            return redirect(patient)
    else:
        data = PatientCreationForm()
    return render(request,
                  template_name='add_patient.html',
                  context={'form': data})
