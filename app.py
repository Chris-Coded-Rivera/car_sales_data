import pandas as pd
import streamlit as st
import scipy.stats
import altair as alt

st.write("""
		# Data Science Web App on Car Sales Dataset
    	This web application has been designed to allow for visitors
	to view the car data sales from 2018-1019.
 
""")

st.header('Car Sales Data')

df = pd.read_csv('clean_car_data.csv')


#creating sidebar for visitors to select vehicle values and view data
st.sidebar.header('Input Vehicle Details')
selected_make = st.sidebar.multiselect('Make', df['make'].unique())

if selected_make:
    filtered_data = df[df['make'].isin(selected_make)]
    models = filtered_data['model'].unique()
    
    # Sidebar for selecting models
    selected_models = st.sidebar.multiselect('Select Vehicle Model(s)', models)
else:
    st.sidebar.write("Please select at least one make.")
    
if selected_models:
    filtered_models_data = filtered_data[filtered_data['model'].isin(selected_models)]
    years = filtered_models_data['model_year'].unique()
    
    # Sidebar for selecting model years
selected_years = st.sidebar.multiselect('Select Model Year(s)', years)

        # Show filtered results
if selected_years:
    final_data = filtered_models_data[filtered_models_data['model_year'].isin(selected_years)]
    st.write(final_data)
else:
    st.write("Please select at least one model year.")

# filtered_df = df[df['make'] == selected_make] #filter out the the selected data

# selected_model = st.sidebar.multiselect('Car Model', filtered_df['model'].unique()) #filtered out unrelated vehicle data from selected values
#model_df = st.sidebar.multiselect('Year', selected_model[selected_model['mode'

#sidebar - model selection
#vehicle_model = st.sidebar.multiselect('Model', selected_model['model']==selected_model.unique())


