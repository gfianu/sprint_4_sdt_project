#!/usr/bin/env python
# coding: utf-8

# # Sprint 4_Software Development Tools
# __________________________________________________________

# In[1]:


# Importing all libraries
import pandas as pd
import numpy as np
import seaborn as sns
import plotly as pl
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import altair as alt
from PIL import Image
import base64


# Retrieving data
vehicles = pd.read_csv('/Users/fianug/Documents/GitHub/sprint_4_sdt_project/vehicles_us.csv')

# creating a category of cars based on class

def car_class(x):
    if x >= 75000:
        return 'luxury vehicle'
    elif x < 75000 and x >= 5000:
        return 'normal vehicle'
    else:
        return 'old vehicle'
    
vehicles['class'] = vehicles['price'].apply(car_class)

# Determining vehicle models 
vehicle_models = vehicles['model'].sort_values().unique()

# Vehicle types
vehicle_types = vehicles['type'].sort_values().unique()

# Vehicle condition
vehicle_condition = vehicles['condition'].sort_values().unique()

# Streamlit introduction page
st.title('Welcome to The Car Dealership!!')

st.markdown("""
This app performs simple analysis on the vehicle inventory!
""")
# Side bar
st.sidebar.header('User Input Features')

# Side bar vehicle type selection
selected_type = st.sidebar.multiselect('Vehicle types',vehicle_types, vehicle_types)

# Side bar vehicle condition
selected_condition = st.sidebar.multiselect('Vehicle condition',vehicle_condition, vehicle_condition)

# Filtering data
types_conditions = vehicles[(vehicles.type.isin(vehicle_types)) & (vehicles.condition.isin(vehicle_condition))]

st.header('Display Vehicles by types and conditions')
st.write('Data Dimension: ' + str(types_conditions.shape[0]) + ' rows and ' + str(types_conditions.shape[1]) + ' columns.')
st.dataframe(types_conditions)


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






