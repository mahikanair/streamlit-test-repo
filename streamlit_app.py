import streamlit as st
import requests
import json

st.title('Iris Flower Prediction')

# Input features
sl = st.slider('Nitrogen', int(0), int(140), int(0))
sw = st.slider('Phosphorus', int(5), int(145), int(5))
pl = st.slider('Potassium', int(5), int(205), int(5))
tl = st.slider('Temperature', float(8.83), float(43.67), float(8.83))
hu = st.slider('Humidity', float(14.26), float(99.98), float(14.26))
ph = st.slider('pH_Value', float(3.51), float(9.93), float(3.51))
rf = st.slider('Rainfall', float(20.22), float(298), float(20.22))

# Update this URL to point to your deployed Flask API
url = "https://crop-classification.onrender.com/predict"

if st.button('Predict'):
    response = requests.post(url, json={'features': [sl, sw, pl, tl, hu, ph, rf]})
    if response.status_code == 200:
        prediction = response.json()['prediction']
        st.success(f'The predicted Iris class is: {prediction}')
    else:
        st.error('Failed to get prediction')
