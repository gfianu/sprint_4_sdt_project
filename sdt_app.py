#!/usr/bin/env python
# coding: utf-8

# # Sprint 4_Software Development Tools
# __________________________________________________________


# Importing all libraries
import pandas as pd
import numpy as np
import plotly as pl
import plotly.express as px
import streamlit as st

# Streamlit introduction page
st.title('Welcome to The Car Dealership!!')

st.markdown("""
This app performs simple analysis on the vehicle inventory of this dealership!
""")
# Side bar
st.sidebar.header('User Input Features')

# Retrieving data
vehicles = pd.read_csv('vehicles_us.csv')

# creating a category of cars based on class
def car_class(x):
    if x >= 75000:
        return 'luxury vehicle'
    elif x < 75000 and x >= 5000:
        return 'normal vehicle'
    else:
        return 'old vehicle'
      
vehicles['class'] = vehicles['price'].apply(car_class)

# Filling in missing values in dataset

#Finding median year for model
median_year = vehicles.groupby('model')['model_year'].transform('median')

# Filling in missing values for model_year
vehicles['model_year'] = vehicles['model_year'].fillna(median_year)

# Finding median cylinder
median_cylinder = vehicles.groupby('model')['cylinders'].transform('median')

# Filling in missing values for cylinders
vehicles['cylinders'] = vehicles['cylinders'].fillna(median_cylinder)

# Finding mean odometer
mean_odometer = vehicles.groupby(['model', 'model_year'])['odometer'].transform('mean')

# Filling in missing values for cylinders
vehicles['odometer'] = vehicles['odometer'].fillna(mean_odometer)

#fill in missing car colors as unknown
vehicles['paint_color'] = vehicles['paint_color'].fillna('unknown')

#Filling in missing values for is_4wd column
vehicles['is_4wd'].unique()

# Only the value 1 is provided in this column.
# This suggests that if 1 means yes, then 0 means no
vehicles['is_4wd'] = vehicles['is_4wd'].fillna(0)

# Determining vehicle models 
vehicle_models = vehicles['model'].sort_values().unique()

# Vehicle types
vehicle_types = vehicles['type'].sort_values().unique()

# Vehicle condition
vehicle_condition = vehicles['condition'].sort_values().unique()

# Side bar vehicle type selection
selected_type = st.sidebar.multiselect('Vehicle types',vehicle_types, vehicle_types)

# Side bar vehicle condition
selected_condition = st.sidebar.multiselect('Vehicle condition',vehicle_condition, vehicle_condition)

# Filtering data
vehicles_filtered = vehicles[(vehicles.type.isin(selected_type)) & (vehicles.condition.isin(selected_condition))]

st.header('Display vehicles by types and conditions')
st.write('Data Dimension: ' + str(vehicles_filtered.shape[0]) + ' rows and ' + str(vehicles_filtered.shape[1]) + ' columns.')
st.dataframe(vehicles_filtered)

# Streamlit data exploration using plotly_express
st.header('Analysis of vehicle types based on price (in USD) and condition')
st.write(px.strip(vehicles, x='type', y = 'price', color = 'condition', hover_name = 'model'))

# Streamlit data exploration using plotly_express
st.header('Analysis on how vehicle condition and fuel affects price (in USD)')
st.write(px.histogram(vehicles, x='fuel', y = 'price', color = 'condition', hover_name = 'model'))

# Streamlit data exploration using plotly_express
st.header('Vehicles based on types and fuel')
st.write(px.histogram(vehicles, x='type', color ='fuel', hover_name = 'model'))

# Streamlit data exploration using plotly_express
st.header('Analysis on how vehicle type and condition affects price')
st.write(px.bar(vehicles, x='type', y = 'price', color = 'condition', hover_name = 'model'))

# Streamlit data exploration using plotly_express
st.header('A sunburst chart of vehicle inventory by fuel, type, and condition')
st.write(px.sunburst(vehicles, color ='model', values = 'price', path= ['fuel','type', 'condition'] , 
            hover_name = 'model_year', height= 700))

# Streamlit data exploration using plotly_express
st.header('A treemap of vehicle inventory by fuel, type, model, condition, and price')
st.write(px.treemap(vehicles, color ='transmission', values = 'odometer', path= ['fuel','type', 'model', 'condition', 'price'] , 
            hover_name = 'model_year', height= 700))

# Streamlit data exploration using plotly_express
st.header('Analysis of vehicle price by type, model, model year, and condition')
st.write(px.scatter(vehicles, y ='model_year', x = 'type', hover_name = 'model', size = 'price', 
           color = 'condition', size_max = 80, height= 700))

st.header('Price analysis')
st.write("""
###### Analyzing what influences price the most        
        """)

# Histogram filtering by fuel, type, model, model_year, condition, transmission
list_for_hist=['fuel', 'type', 'model', 'model_year','condition', 'transmission']

#creating selectbox
choice_for_hist = st.selectbox('Split for price distribution', list_for_hist)

#plotly histogram, where price is filtered by the choice made in the selectbox
fig1 = px.histogram(vehicles, x = 'price', color=choice_for_hist)

#adding tittle
fig1.update_layout(title='<b> Filter car price by {}</b>'.format(choice_for_hist))

#embedding into streamlit
st.plotly_chart(fig1)






