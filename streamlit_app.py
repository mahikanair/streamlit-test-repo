import streamlit as st
import numpy as np
import requests
import pandas as pd
import os

st.title('Crop To Grow Prediction')
st.caption('Enhancing Agricultural Performance Through Advanced Crop Prediction')

st.write("This app aims to maximize crop rotation efficiency and overall agricultural performance by leveraging advanced machine learning techniques for crop classification. With the advent of affordable soil testing kits, it has become feasible for governments to implement this technology to aid farmers in making informed decisions about their crop choices. By using this app, farmers can optimize their crop yields, enhance soil health, and achieve better agricultural productivity.")
st.write("Here are the different prediction types:")
st.caption('Single Crop Prediction')
st.write("n the Single Crop Prediction section, users can manually input soil and weather parameters to get a prediction for the most suitable crop to plant - by typing in the numbers or using the slider.")
st.caption('Multiple Crops Prediction')
st.write("In the Multiple Crops Prediction section, users can upload a CSV file containing multiple sets of soil and weather parameters. This feature is particularly useful for larger farms or agricultural planning over a wide area.")
st.caption("To see information on the dataset, check out the sidebar!")
# Add a sidebar
st.sidebar.title("The Crop Classification Dataset")

# Add text to the sidebar
st.sidebar.header("Information")

# Use markdown for better formatting
st.sidebar.markdown("""
**The Crop Recommendation Dataset** is a comprehensive dataset designed to assist in the optimal selection of crops based on soil and weather conditions. 

It contains **2,200 rows** of data, each representing a unique combination of agricultural parameters and the corresponding recommended crop. 

The dataset includes seven key features:
- Nitrogen content ratio in the soil
- Phosphorus content ratio in the soil
- Potassium content ratio in the soil
- Temperature (°C)
- Relative humidity (%)
- pH value of the soil
- Rainfall (mm)

These features are crucial for determining the suitability of various crops. The dataset categorizes crops into 22 different classes, providing a wide range of options for agricultural planning. By analyzing this dataset, one can leverage advanced machine learning techniques to make informed decisions about the most suitable crops to grow under specific soil and weather conditions, thereby enhancing crop yields, improving soil health, and increasing overall agricultural productivity.

This dataset is available on Kaggle and serves as a valuable resource for researchers, agricultural planners, and farmers aiming to maximize crop rotation efficiency and agricultural performance.
""")

st.sidebar.header("Crops Present:")
# Add crops list with bullet points
st.sidebar.markdown("""
- Apple
- Banana
- Blackgram
- Chickpea
- Coconut
- Coffee
- Cotton
- Grapes
- Jute
- Kidney Beans
- Lentil
- Maize
- Mango
- Moth Beans
- Mung Beans
- Muskmelon
- Orange
- Papaya
- Pigeon Peas
- Pomegranate
- Rice
- Watermelon
""")

# Add a clickable link
dataset_url = "https://www.kaggle.com/datasets/varshitanalluri/crop-recommendation-dataset"
st.sidebar.markdown(f"[Link to the dataset]({dataset_url})")
# Create a selection box for single or multiple predictions
prediction_type = st.selectbox('Select Prediction Type', ['Single Crop Prediction', 'Multiple Crops Prediction'])

def input_feature(label, min_value, max_value, value):
    option = st.radio(f'{label} input method', ('Slider', 'Number Input'))
    if option == 'Slider':
        return st.slider(label, min_value, max_value, value)
    else:
        return st.number_input(label, min_value=min_value, max_value=max_value, value=value)

if prediction_type == 'Single Crop Prediction':
    st.header('Single Crop Prediction')
    # Input features for single crop prediction with both slider and input box
    sl = input_feature('Nitrogen', 0, 140, 0)
    sw = input_feature('Phosphorus', 5, 145, 5)
    pl = input_feature('Potassium', 5, 205, 5)
    tl = input_feature('Temperature', float(9), float(43), float(9))
    hu = input_feature('Humidity', float(15), float(99), float(15))
    ph = input_feature('pH Value', float(4), float(9), float(4))
    rf = input_feature('Rainfall', float(21), float(298), float(21))

    # Update this URL to point to your deployed Flask API
    url = "https://crop-class.onrender.com/predict"

    if st.button('Predict'):
        # Construct the correct JSON payload for single crop prediction
        payload = {
            'Nitrogen': sl,
            'Phosphorus': sw,
            'Potassium': pl,
            'Temperature': tl,
            'Humidity': hu,
            'pH_Value': ph,
            'Rainfall': rf
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            prediction = response.json().get('prediction', 'No prediction found')
            st.success(f'The crop one should grow here is: {prediction}')
            # Extract the first word from the prediction
            predicted_crop = prediction.split()[0]
            
            # Define the path to the crop images directory
            image_directory = "crop_image"
            
            # Check for image files in the directory
            image_path = None
            for ext in ["jpg", "jpeg"]:
                potential_path = os.path.join(image_directory, f"{predicted_crop}.{ext}")
                if os.path.exists(potential_path):
                    image_path = potential_path
                    break
            
            if image_path:
                 #Display the image
                st.image(image_path)
            else:
                st.warning(f'No image found for {predicted_crop}')
        else:
            st.error('Failed to get prediction')
            
        

elif prediction_type == 'Multiple Crops Prediction':
    expected_ranges = {
        'Nitrogen': (0, 140, int),
        'Phosphorus': (5, 145, int),
        'Potassium': (5, 205, int),
        'Temperature': (9.0, 43.0, float),
        'Humidity': (15.0, 99.0, float),
        'pH_Value': (4.0, 9.0, float),
        'Rainfall': (21.0, 298.0, float)
    }
    def validate_data(df, expected_ranges):
        validation_errors = []
        for index, row in df.iterrows():
            for col, (min_val, max_val, dtype) in expected_ranges.items():
                value = row[col]
                if not (min_val <= value <= max_val):
                    validation_errors.append(f"Row {index + 1}, Column '{col}': Value {value} out of range ({min_val}-{max_val}).")
        return validation_errors
    
    
    st.header('Multiple Crops Prediction')
    st.write('This is for when you would like to do this for multiple files. A sample csv has been provided here for you to dowload and take a look at to see the format and fill in as you require.')
    st.write('You will be able to see your uploaded csv to make sure there were no mistakes.')
    st.download_button(
        label="Download Sample CSV",
        data='sample.csv',
        file_name='sample.csv',
        mime='text/csv'
    )
    # Create a file uploader for multiple crop prediction
    uploaded_file = st.file_uploader('Upload CSV file', type=['csv'])

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)

        # Display the uploaded CSV
        st.write('Uploaded CSV data:')
        st.dataframe(data)

        # Check if the number of columns matches the expected number
        expected_num_columns = 7  # Number of required input features
        if data.shape[1] == expected_num_columns:
            data.columns = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH_Value', 'Rainfall']
            try:
                # Convert the first three columns to int
                for col in data.columns[:3]:
                    data[col] = data[col].astype(int)
                
                # Convert the next four columns to float
                for col in data.columns[3:7]:
                    data[col] = data[col].astype(float)
            except ValueError as e:
                # Identify the problematic column
                problematic_column = col
                st.error(f"Error converting column '{problematic_column}' to its target type: {e}. Make sure you are giving the integers for Nitrogren Phosphorous and Potassium and decimal values for the rest!")
            else: 
                errors = validate_data(data, expected_ranges)
                if errors:
                    st.error("Validation errors found in the CSV:")
                    for error in errors:
                        st.error(error)
                    
                else:
                    # Update this URL to point to your deployed Flask API for single predictions
                    url = "https://crop-class.onrender.com/predict"
                    if st.button('Predict Multiple Crops'):
                        columns = st.columns(2)  # Create two columns
                        col_index = 0  # To keep track of the current column
                
                        for index, row in data.iterrows():
                            payload = {
                                'Nitrogen': row[0],
                                'Phosphorus': row[1],
                                'Potassium': row[2],
                                'Temperature': row[3],
                                'Humidity': row[4],
                                'pH_Value': row[5],
                                'Rainfall': row[6]
                            }
                            response = requests.post(url, json=payload)
                            if response.status_code == 200:
                                prediction = response.json().get('prediction', 'No prediction found')
                                predicted_crop = prediction.split()[0]
                
                                # Define the path to the crop images directory
                                image_directory = "crop_image"
                
                                # Check for image files in the directory
                                image_path = None
                                for ext in ["jpg", "jpeg"]:
                                    potential_path = os.path.join(image_directory, f"{predicted_crop}.{ext}")
                                    if os.path.exists(potential_path):
                                        image_path = potential_path
                                        break
                
                                # Select the current column
                                with columns[col_index]:
                                    st.write(f'For Field {index}')
                                    st.write(f'One should grow {prediction}')
                                    if image_path:
                                        st.image(image_path, caption=f'{predicted_crop} Image')
                                    else:
                                        st.warning(f'No image found for {predicted_crop}')
                
                                # Move to the next column
                                col_index += 1
                                if col_index >= 2:
                                    col_index = 0
                                    st.markdown('---')
                                    columns = st.columns(2)  # Create new columns for the next row
                                    
                
                            else:
                                st.error(f'Failed to get prediction for row {index + 1}')
