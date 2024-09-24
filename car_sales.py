import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt

st.write("""
		# Data Science Web App on Car Sales Dataset
    	This web application has been designed to allow for visitors
	to view a dataset from car sales data from 2018-1019.
 
""")

st.divider() #display line to divide the sections of the site

# Load dataset
df = pd.read_csv('cars_clean.csv')

modify = st.checkbox("Add Filters") #assign variable to checkbox

def filter_dataframe(df): #create function for checkbox
    options = st.multiselect( "Select Vehicle Make(s)",
        (df['make'].unique()),placeholder="select vehicle make(s)"
    )
    st.write(options)
    return df[df['make'].isin(options)] if options else df

if modify: #if/and statement for checkbox to call function if checked. Display DF if not
    filtered_df = filter_dataframe(df)
    if filtered_df.empty:
        st.write("No data available for the selected filters.")
    else:
        st.dataframe(filtered_df) 
else:
    st.dataframe(df)
    st.write("""
             Select 'Add Filters' to filter vehicle make. This will only affect the data on the table. The charts data will not be affected
             """)
st.divider()
    
st.write("""
    Let's check out average sales price per model by make
         
    """)
#scatter plot showing average price of each model, within each vehicle make category, showing the model name when curser hovers over dots
avg_price = df.groupby(['make','model']).agg({'price':'mean'}).reset_index()
avg_make = df.groupby('make').agg({'price':'mean'}).reset_index()
make = st.checkbox("Show Average Make Sales")
if make:
    fig_1 = px.scatter(x=avg_make['make'], y=avg_make['price'],labels={'x': 'Vehicle Make','y': 'Purchase Price($)'})
    fig_1.update_layout(title="Average Sales Price")
    st.plotly_chart(fig_1)

else:
    fig_2 = px.scatter(x=avg_price['make'], y=avg_price['price'],hover_data=[avg_price['model']],labels={'x': 'Vehicle Make','y': 'Purchase Price($)','hover_data_0':'Model'})
    fig_2.update_layout(title="Average Sales Price")
    st.write("""
             Checking the box will display scatterplot of average sales of each vehicle make
             """)
    st.plotly_chart(fig_2)

st.divider()

st.write("""
         Simple distribution of sales for vehicle color to see the popularity of each color
         """)
#histogram for distribution of the colors of cars sold
known_color = st.checkbox('Exclude Unknown Paint Color')
if known_color:
    colors = df[df['paint_color'] != 'unknown']
    st.markdown("##### Distribution of known vehicle color sales")
    fig_3 = alt.Chart(colors).mark_bar().encode(alt.X("paint_color", title='Vehicle Color'),alt.Y('count()', title='Count'))
    st.altair_chart(fig_3, use_container_width=True)
else:
    fig_4 = alt.Chart(df).mark_bar().encode(alt.X("paint_color", title='Vehicle Color'),alt.Y("count()", title='Count'))
    st.write("""
             Checking the abox will show the distribution of the vehicle colors with 'unknown' values removed
             """)
    st.markdown("##### Distribution of all vehicle color sales")
    st.altair_chart(fig_4, use_container_width=True)