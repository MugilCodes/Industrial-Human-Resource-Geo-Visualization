import pandas as pd
import streamlit as st
import folium
import plotly.express as px
import matplotlib.pyplot as plt
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static  

# Load the dataset once
data = pd.read_csv("C:/Users/DELL/Desktop/CT/final_HR.csv")

# Sidebar selections
st.sidebar.title("Select Options")
unique_states = sorted(data['State'].unique())
selected_state = st.sidebar.selectbox("Select State", unique_states)

filtered_districts = sorted(data[data['State'] == selected_state]['District'].unique())
selected_district = st.sidebar.selectbox("Select District", filtered_districts)

# Filter state and district data
state_data = data[data['State'] == selected_state]
district_data = state_data[state_data['District'] == selected_district]

# Display filtered data
st.subheader(f"Data for {selected_state} - {selected_district}")
st.write(district_data)

# Map Visualization
st.subheader("Worker Distribution Map")

# Check if latitude & longitude exist
if 'latitude' in data.columns and 'longitude' in data.columns:
    india_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    marker_cluster = MarkerCluster().add_to(india_map)

    for _, row in district_data.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"{row['District']} - Workers: {row['MainWorkersTotalPersons']}"
        ).add_to(marker_cluster)

    # Display Folium map in Streamlit
    folium_static(india_map)
else:
    st.warning("Latitude & Longitude data missing!")

# Plotly Chart for Workers
st.subheader("Worker Count Analysis")
fig = px.bar(
    district_data,
    x="District",
    y=["MainWorkersTotalPersons", "MainWorkersRuralPersons", "MainWorkersUrbanPersons"],
    labels={"value": "Workers", "variable": "Worker Type"},
    title=f"Worker Distribution in {selected_district}",
    barmode="group"
)
st.plotly_chart(fig)
