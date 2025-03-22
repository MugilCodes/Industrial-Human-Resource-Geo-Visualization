import pandas as pd
import streamlit as st
import folium
import plotly.express as px
import matplotlib.pyplot as plt
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static  
  
# Load the dataset once
#data = pd.read_csv(r"C:\Users\DELL\Downloads\streamlit\env\Scripts\final_HR.csv")
data=pd.read_csv(r"C:\Users\DELL\Desktop\HRM_with_latlong.csv")

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
if 'Latitude' in data.columns and 'Longitude' in data.columns:
    # Filter out missing values
    valid_district_data = district_data.dropna(subset=['Latitude', 'Longitude'])

    if not valid_district_data.empty:
        # Get the first valid latitude and longitude to center the map
        center_lat = valid_district_data['Latitude'].iloc[0]
        center_lon = valid_district_data['Longitude'].iloc[0]
    else:
        # Default to India's center if no valid data
        center_lat, center_lon = 20.5937, 78.9629  

    # Create a map centered on the selected district
    district_map = folium.Map(location=[center_lat, center_lon], zoom_start=5)  
    marker_cluster = MarkerCluster().add_to(district_map)

    # Add markers for each worker location
    for _, row in valid_district_data.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['District']} - Workers: {row['MainWorkersTotalPersons']}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(marker_cluster)

    # Display the updated Folium map
    folium_static(district_map)

else:
    st.warning("Latitude & Longitude data missing!")


# Pie Chart for Worker Distribution
st.subheader("Worker Proportion Analysis")

# Prepare data for pie chart
pie_data = {
    "Category": ["Main Workers Total", "Main Workers Rural", "Main Workers Urban"],
    "Count": [
        district_data["MainWorkersTotalPersons"].sum(),
        district_data["MainWorkersRuralPersons"].sum(),
        district_data["MainWorkersUrbanPersons"].sum()
    ]
}

pie_df = pd.DataFrame(pie_data)

# Plotly Chart for Main & Marginal Workers
st.subheader("Main vs. Marginal Worker Analysis")

fig_workers = px.bar(
    district_data,
    x="District",
    y=["MainWorkersTotalPersons", "MarginalWorkersTotalPersons"],
    labels={"value": "Workers", "variable": "Worker Type"},
    title=f"Comparison of Main & Marginal Workers in {selected_district}",
    barmode="group",  # Group bars for easy comparison
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig_workers, use_container_width=True)



st.subheader("Main vs. Marginal Worker Proportion")

# Prepare data for pie chart
pie_data_main = {
    "Category": ["Main Workers Rural", "Main Workers Urban"],
    "Count": [
        district_data["MainWorkersRuralPersons"].sum(),
        district_data["MainWorkersUrbanPersons"].sum()
    ]
}

pie_data_marginal = {
    "Category": ["Marginal Workers Rural", "Marginal Workers Urban"],
    "Count": [
        district_data["MarginalWorkersRuralPersons"].sum(),
        district_data["MarginalWorkersUrbanPersons"].sum()
    ]
}

pie_df_main = pd.DataFrame(pie_data_main)
pie_df_marginal = pd.DataFrame(pie_data_marginal)

# Create Pie Charts
fig_pie_main = px.pie(
    pie_df_main,
    names="Category",
    values="Count",
    title=f"Main Worker Proportion in {selected_district}",
    color_discrete_sequence=px.colors.qualitative.Set1
)

fig_pie_marginal = px.pie(
    pie_df_marginal,
    names="Category",
    values="Count",
    title=f"Marginal Worker Proportion in {selected_district}",
    color_discrete_sequence=px.colors.qualitative.Set2
)

# Display Pie Charts Side by Side
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_pie_main, use_container_width=True)
with col2:
    st.plotly_chart(fig_pie_marginal, use_container_width=True)


# Create Pie Chart
fig_pie = px.pie(
    pie_df,
    names="Category",
    values="Count",
    title=f"Worker Proportion in {selected_district}",
    color_discrete_sequence=px.colors.qualitative.Set1
)

# Display Pie Chart
st.plotly_chart(fig_pie, use_container_width=True)



# Plotly Chart for Workers
st.subheader("Worker Count Analysis")
fig =px.bar(
    district_data,
    x="District",
    y=["MainWorkersTotalPersons", "MainWorkersUrbanPersons", "MainWorkersRuralPersons"],
    labels={"value": "Workers", "variable": "Worker Type"},
    title=f"Worker Distribution in {selected_district}",
    barmode="group",
    color_discrete_sequence=px.colors.qualitative.Set1
)
st.plotly_chart(fig, use_container_width=True)
