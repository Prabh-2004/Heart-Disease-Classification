import os
import streamlit as st
import pandas as pd
import numpy as np
from src.pipelines.prediction_pipeline import PredictionPipeline

st.set_page_config(page_title="Heart Disease Prediction Model", layout='centered')

st.title("Predict Heart Disease")
st.write("This app predicts whether a patient has Heart Disease or not based on the following set of features, using a Machine learning Classification Model.")

if "training_status" not in st.session_state:
    st.session_state.training_status = False

if not st.session_state.training_status:
    with st.spinner("Training the Model..."):
        os.system("python main.py")
    st.session_state.training_status = True


age = int(st.number_input(label="Age"))
sex = st.text_input("Sex")
chest_pain_type =st.text_input("Chest Pain type")
resting_blood_pressure =int(st.number_input("Resting Blood Pressure"))
cholestoral = int(st.number_input("Cholestoral"))
fasting_blood_sugar =st.text_input("Fasting Blood Sugar")
rest_ecg =st.text_input("Rest ECG")
Max_heart_rate = int(st.number_input("Max Heart Rate"))
exercise_induced_angina =st.text_input("Exercise Induced Angina")
oldpeak = float(st.number_input("Old Peak"))
slope =st.text_input("Slope")
vessels_colored_by_flourosopy = st.text_input("Vessels Colored by Flourosopy")
thalassemia = st.text_input("Thalassemia")

feature_name = ["age", "sex", "chest_pain_type", "resting_blood_pressure", "cholestoral", "fasting_blood_sugar", "rest_ecg", "Max_heart_rate", "exercise_induced_angina", "oldpeak", "slope", "vessels_colored_by_flourosopy", "thalassemia"]

feature_data = [[age, sex, chest_pain_type, resting_blood_pressure, cholestoral, fasting_blood_sugar, rest_ecg, Max_heart_rate, exercise_induced_angina, oldpeak, slope, vessels_colored_by_flourosopy, thalassemia]]

data = pd.DataFrame(data=feature_data, columns=feature_name)

# data = pd.DataFrame([{
#     "age": age,
#     "sex": sex,
#     "chest_blood_pain": chest_blood_pain,
#     "resting_blood_pressure": resting_blood_pressure,
#     "cholestoral":  cholestoral,
#     "fasting_blood_sugar": fasting_blood_sugar,
#     "rest_ecg":pain_type
#     "Max_heart_rate":  Max_heart_rate,
#     "exercise_induced_angina": exercise_induced_angina,
#     "oldpeak":  oldpeak,
#     "slope": slope,
#     "vessels_colored_by_flourosopy":  vessels_colored_by_flourosopy,
#     "thalassemia":  thalassemia,
# }])

st.divider()

if st.button("Predict Heart Disease"):
    with st.spinner("Predicting..."):
        obj = PredictionPipeline()
        prediction = obj.predict(data)

    st.success(f"The Predicted Value is: {prediction}")