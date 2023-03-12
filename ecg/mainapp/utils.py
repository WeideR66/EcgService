import numpy as np
import wfdb
from biosppy.signals import ecg
import joblib
import pandas as pd
from django.conf import settings


def save_image(file_name, image_path):
    record = wfdb.rdrecord(file_name)
    fig = wfdb.plot_wfdb(record=record, return_fig=True)
    axes = fig.gca()
    axes.set_xlim([0, 10])
    print('Success')
    fig.savefig(image_path)


def get_data(file):
    normal_sinus_rhythm = joblib.load(settings.DATASETS_URL + "normal_sinus_rhythm.joblib")
    arrhythmia = joblib.load(settings.DATASETS_URL + "arrhythmia.joblib")
    atrial_fibrillation = joblib.load(settings.DATASETS_URL + "atrial_fibrillation.joblib")
    malignant_ventricular_ectopy = joblib.load(settings.DATASETS_URL + "malignant_ventricular_ectopy.joblib")
    supraventricular_arrhythmia = joblib.load(settings.DATASETS_URL + "supraventricular_arrhythmia.joblib")

    signal_list = []

    for i in range(len(file)):
        record = wfdb.rdrecord(file[:-4])
        fs = record.__dict__['fs']
        channel_number = record.__dict__['n_sig']

        for j in range(channel_number):
            signal = record.__dict__['p_signal'][:, j][0:100000]
            out = ecg.ecg(signal=signal, sampling_rate=fs, show=False)
            out_array = out['templates']

            for k in range(out_array.shape[0]):
                signal_list.append(out_array[k])

    from scipy import signal
    rescaled_list = []
    for i in range(len(signal_list)):
        rescaled_list.append(signal.resample(signal_list[i], 76))

    X = np.array(rescaled_list)
    normal_sinus_rhythm = np.mean(normal_sinus_rhythm.predict(X), axis=None)
    arrhythmia = np.mean(arrhythmia.predict(X), axis=None)
    atrial_fibrillation = np.mean(atrial_fibrillation.predict(X), axis=None)
    malignant_ventricular_ectopy = np.mean(malignant_ventricular_ectopy.predict(X), axis=None)
    supraventricular_arrhythmia = np.mean(supraventricular_arrhythmia.predict(X), axis=None)
    column_list = [file,
                   round(normal_sinus_rhythm, 2),
                   round(arrhythmia, 2),
                   round(atrial_fibrillation, 2),
                   round(malignant_ventricular_ectopy, 2),
                   round(supraventricular_arrhythmia, 2)
                   ]
    df = pd.DataFrame(np.column_stack(column_list), columns=['file name',
                                                             'normal sinus rhythm',
                                                             'arrhythmia',
                                                             'atrial fibrillation',
                                                             'malignant ventricular ectopy',
                                                             'supraventricular arrhythmia'
                                                             ])
    return df
