from django.db import models
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from .utils import get_data, save_image


def user_directory_path(instance, filename):
    return f'patient_{instance.patient.pk}/{filename}'


class Doctor(models.Model):
    doctor_name = models.CharField(max_length=50, verbose_name='Имя')
    doctor_surname = models.CharField(max_length=50, verbose_name='Фамилия')
    job_title = models.CharField(max_length=50, verbose_name='Должность')

    def __str__(self):
        return f"{self.doctor_surname} {self.doctor_name}"


class Patient(models.Model):
    doctor = models.ForeignKey('Doctor',
                               on_delete=models.PROTECT,
                               verbose_name='Лечащий врач',
                               blank=True)
    patient_name = models.CharField(max_length=50, verbose_name='Имя пациента')
    patient_surname = models.CharField(max_length=50, verbose_name='Фамилия пациента')
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата проведения ЭКГ')

    def __str__(self):
        return f"{self.patient_surname} {self.patient_name}"

    def get_absolute_url(self):
        return reverse('patient', kwargs={'patient_id': self.pk})


class EcgData(models.Model):
    patient = models.OneToOneField(Patient,
                                   on_delete=models.CASCADE,
                                   verbose_name='Пациент',
                                   null=True)
    ecg_hea_file = models.FileField(upload_to=user_directory_path,
                                    blank=True,
                                    verbose_name='Данные ЭКГ',
                                    validators=[FileExtensionValidator(
                                        allowed_extensions=('hea',),
                                        message='Файлы должны иметь разрешение .hea'
                                    )])
    ecg_dat_file = models.FileField(upload_to=user_directory_path,
                                    blank=True,
                                    verbose_name='Данные ЭКГ',
                                    validators=[FileExtensionValidator(
                                        allowed_extensions=('dat',),
                                        message='Файлы должны иметь разрешение .dat'
                                    )])

    def __str__(self):
        return f'{self.ecg_hea_file}'


class Results(models.Model):
    patient = models.OneToOneField(Patient,
                                   on_delete=models.CASCADE,
                                   verbose_name='Пациент',
                                   blank=True)
    ecg_image = models.ImageField(upload_to=user_directory_path,
                                  blank=True,
                                  verbose_name='Изображение ЭКГ')
    normal = models.FloatField(verbose_name='Нормальный синусовый ритм')
    arrhythm = models.FloatField(verbose_name='Аритмия')
    atrial_fib = models.FloatField(verbose_name='Мерцательная аритмия')
    mal_vent_ect = models.FloatField(verbose_name='Злокачественная желудочковая эктопия')
    sup_arrh = models.FloatField(verbose_name='Наджелудочковая аритмия')


@receiver(post_save, sender=EcgData)
def fill_data(sender, instance, **kwargs):
    patient_pk = instance.patient.pk
    file_path = str(instance.ecg_hea_file)
    data = get_data('media\\' + file_path)
    save_image('media\\' + file_path[:-4],
               f"media\\patient_{patient_pk}\\ecgimage.png")
    obj = Results(
        patient_id=patient_pk,
        ecg_image=f'patient_{patient_pk}\\{"ecgimage.png"}',
        normal=float(data['normal sinus rhythm']),
        arrhythm=float(data['arrhythmia']),
        atrial_fib=float(data['atrial fibrillation']),
        mal_vent_ect=float(data['malignant ventricular ectopy']),
        sup_arrh=float(data['supraventricular arrhythmia'])
    )
    obj.save()

