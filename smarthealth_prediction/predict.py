from flask import render_template, request
import pandas as pd
import numpy as np
from numpy import loadtxt
from keras.models import load_model


def get_prediction(age, gender, race, ethnicity, obesity, heart_rate, d_bp, s_bp, ew):
    saved_blend1 = load_model("modelv4.h5")
    data = {'age': age,
            'Female': 0,
            'Male': 0,
            'White': 0,
            'Asian': 0,
            'Black': 0,
            'Native': 0,
            'Other': 0,
            'Hispanic': 0,
            'Nonhispanic': 0,
            'Obesity': obesity,
            'Heart Rate Avg': heart_rate,
            'Diastolic BP': d_bp,
            'Systolic BP': s_bp,
            'Erythrocyte Width': ew
            }
    patient = pd.DataFrame.from_records([data])
    patient = patient.replace({race: 0, ethnicity: 0, gender: 0}, 1)

    y = saved_blend1.predict(patient)

    return y


def predict():
    print(request.args)
    res = None
    for arg in ('age', 'gender', 'race', 'ethnicity', 'obesity', 'heart_rate', 'd_bp', 's_bp', 'ew'):
        if arg not in request.args:
            return "Corrupted data!"

    age = int(request.args["age"])
    gender = request.args["gender"]
    race = request.args["race"]
    ethnicity = request.args["ethnicity"]
    obesity = int(request.args["obesity"])
    heart_rate = float(request.args["heart_rate"])
    d_bp = float(request.args["d_bp"])
    s_bp = float(request.args["s_bp"])
    ew = float(request.args["ew"])

    p = get_prediction(age, gender, race, ethnicity, obesity, heart_rate, d_bp, s_bp, ew)

    if res is not None:
        return res
    elif p:
        return "Positive"
    else:
        return "Negative"
