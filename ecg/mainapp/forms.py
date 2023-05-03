from django import forms
from django.core.validators import FileExtensionValidator
from django.contrib.auth.forms import AuthenticationForm
from .models import Doctor


class PatientCreationForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(),
                                    required=False,
                                    label='Врач',
                                    widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(max_length=50,
                           label='Имя пациента',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    surname = forms.CharField(max_length=50,
                              label='Имя пациента',
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    files = forms.FileField(label='Данные ЭКГ',
                            widget=forms.ClearableFileInput(attrs={'class': 'form-control',
                                                                   'multiple': True}),
                            validators=[FileExtensionValidator(
                                                               allowed_extensions=('hea', 'dat'),
                                                               message='Файлы должны иметь разрешение .hea/.dat'
                                                               )])


class UserAuthForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}
                               ))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control'}
                               ))