import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt

st.write("""
		# Data Science Web App on Car Sales Dataset
    	This web application has been designed to allow for visitors
	to view a dataset from car sales data from 2018-1019.
 
""")

st.divider()

# Load dataset
data = pd.read_csv('cars_clean.csv')

def filter_dataframe(df: data) -> data:
    modify = st.checkbox("Add filters")
    if not modify:
        return df
    df = df.copy()
    modification_container = st.container()
    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            if df['make'].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {df['make']}",
                    df['make'].unique(),
                    default=list(df['make'].unique()),
            )
                df = df[df['make'].isin(user_cat_input)]
    return df
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

selected_makes = st.sidebar.multiselect('Select Vehicle Make(s)', makes)
updated_data = data[data['make'].isin(selected_makes)]
# Filter the dataset based on selected makes

st.write("### Vehicle Data")
st.dataframe(updated_data)  # Display the data as a table

st.divider()
    
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
    fig_2 = px.scatter(x=avg_price['make'], y=avg_price['price'],hover_data=[avg_price['model']],labels={'x': 'Vehicle Make','y': 'Purchase Price($)','hover_data_0':'Model'})
    fig_2.update_layout(title="Average Sales Price")
    st.plotly_chart(fig_2)

st.divider()

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
    fig_4 = alt.Chart(data).mark_bar().encode(alt.X("paint_color", title='Vehicle Color'),alt.Y("count()", title='Count'))
    st.altair_chart(fig_4, use_container_width=True)