import pandas as pd
import streamlit as st
import scipy.stats
import altair as alt

st.write(
	"""
    This web application has been designed to allow for visitors to view the car data sales from 2018-1019. 
	"""

st.header('Car Sales Data')

df = pd.read_csv('https://github.com/Chris-Coded-Rivera/car_sales_data/blob/main/vehicles_us.csv')


