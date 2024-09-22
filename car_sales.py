import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt

st.write("""
		# Data Science Web App on Car Sales Dataset
    	This web application has been designed to allow for visitors
	to view a dataset from car sales data from 2018-1019.
 
""")

# Load dataset
data = pd.read_csv('cars_clean.csv')

# Sidebar for selecting makes
st.sidebar.header("Select Vehicle(s)")

# Get unique makes from the dataset
makes = data['make'].unique()
selected_makes = st.sidebar.multiselect('Select Vehicle Make(s)', makes)

# Filter the dataset based on selected makes
if selected_makes:
    filtered_data = data[data['make'].isin(selected_makes)]
    
    # Sidebar for selecting models based on selected makes
    models = filtered_data['model'].unique()
    selected_models = st.sidebar.multiselect('Select Vehicle Model(s)', models)

    # Filter the dataset based on selected models
    if selected_models:
        filtered_models_data = filtered_data[filtered_data['model'].isin(selected_models)]
        
        # Sidebar for selecting model years based on selected models
        years = filtered_models_data['model_year'].unique()
        selected_years = st.sidebar.multiselect('Select Model Year(s)', years)

        # Show filtered results based on selections
        if selected_years:
            final_data = filtered_models_data[filtered_models_data['model_year'].isin(selected_years)]
            st.write("### Vehicle Data")
            st.dataframe(final_data)  # Display the data as a table
        else:
            st.write("Please select at least one model year.")
    else:
        st.write("Please select at least one model.")
else:
    st.sidebar.write("Please select at least one make.")
    
st.write("""
    Let's check out average sales price per model by make
         
    """)
#scatter plot showing average price of each model, within each vehicle make category, showing the model name when curser hovers over dots
avg_price = data.groupby(['make','model']).agg({'price':'mean'}).reset_index()
avg_make = data.groupby('make').agg({'price':'mean'}).reset_index()
make = st.checkbox("Show Average Make Sales")
if make:
    fig_1 = px.scatter(x=avg_make['make'], y=avg_make['price'],labels={'x': 'Vehicle Make','y': 'Purchase Price($)'})
    fig_1.update_layout(title="Average Sales Price")
    st.plotly_chart(fig_1)

else:
    fig_2 = px.scatter(x=avg_price['make'], y=avg_price['price'],hover_data=[avg_price['model']],labels={'x': 'Vehicle model','y': 'Purchase Price($)','hover_data_0':'Model'})
    fig_2.update_layout(title="Average Sales Price")
    st.plotly_chart(fig_2)

st.write("""
         Simple distribution of sales for vehicle color to see the popularity of each color
         """)

known_color = st.checkbox('Exclude Unknown Paint Color')
if known_color:
    colors = data[data['paint_color'] != 'unknown']
    st.markdown("##### Distribution of known vehicle color sales")
    fig_3 = alt.Chart(colors).mark_bar().encode(alt.X("paint_color", title='Vehicle Color'),alt.Y('count()', title='Count'))
    st.altair_chart(fig_3, use_container_width=True)
else:
    st.markdown("##### Distribution of all vehicle color sales")
    fig_4 = alt.Chart(data).mark_bar().encode(alt.X("paint_color", title='Vehicle Color'),alt.Y("count()" title='Count'))
    st.altair_chart(fig_4, use_container_width=True)

# make = st.checkbox('Display Data by Vehicle Make')
# if make:
#     show = 'make'
#     st.markdown('##### A histogram of vehicle conditions based on the vehicle's make')
#     fig = px.histogram(vehicles, x="condition", color=show, barmode='group')
#     fig.update_layout(title_text='Vehicle Condition by Make', xaxis_title='Condition', yaxis_title='Number of Vehicles')
# else:
#     show = 'model'
#     st.markdown('##### A histogram of vehicle conditions based on the vehicle's model')
#     fig = px.histogram(vehicles, x="condition", color=show, barmode='group')
#     fig.update_layout(title_text='Vehicle Condition by Model', xaxis_title='Condition', yaxis_title='Number of Vehicles')