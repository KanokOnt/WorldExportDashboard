import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
world_export_data = pd.read_csv('world_export_data.csv')

with st.sidebar:
    st.logo(
    "reshot-icon-adverts-H429KN5RZD.svg",size = "large"
    )
    st.title("World Export Data Visualization")
    st.write("This app displays export data by country and region with interactive charts.")

    # Get the years for the selected data
    years = list(range(int(world_export_data['Year'].min()), int(world_export_data['Year'].max()) + 1))

    # Select year range using slider
    start_year, end_year = st.select_slider(
        "Select a range of years",
        options=years,
        value=(min(years), max(years))  # Default to full range
    )

    regions = world_export_data['Continent of the territory'].unique()
    region_filter = st.segmented_control(
        "Region", regions, selection_mode="multi",default = regions)



    # Get the countries based on selected regions
    countries = world_export_data[world_export_data['Continent of the territory'].isin(region_filter)]['English Name'].unique()
    country_filter = st.multiselect("Select Country", options=countries, default=countries)


    filtered_data = world_export_data[
        (world_export_data['Continent of the territory'].isin(region_filter)) & 
        (world_export_data['English Name'].isin(country_filter)) & 
        (world_export_data['Year'].between(start_year, end_year))
    ]

map_filtered_data = filtered_data.groupby(["Year","Continent of the territory","English Name","ISO 3 country code"]
                                            , as_index=False).agg({
                                            "Export_Amount": "sum"})


# Create a map chart for export amount by country
st.subheader(f"Export Amount by Country ({', '.join(map(str, region_filter))})")
fig_map = px.choropleth(map_filtered_data, 
                        locations="ISO 3 country code", 
                        color="Export_Amount", 
                        hover_name="English Name",
                        hover_data=["Export_Amount"],
                        color_continuous_scale="Greens",
                        projection="natural earth")
st.plotly_chart(fig_map)

fig_map.update_geos(
    showcountries=True,   # Show country borders
    showcoastlines=True,  # Show coastlines
    showland=True,        # Ensure land is visible
    landcolor="whitesmoke",
    projection_scale=2  # Adjust to fit more area
)



line_filtered_data = filtered_data.groupby(["Year","Continent of the territory"]
                                            , as_index=False).agg({
                                            "Export_Amount": "sum"})

# Create a trendline chart for export by year and region
st.subheader(f"Export Trend by Year and Region ({', '.join(map(str, region_filter))})")
fig_trend = px.line(line_filtered_data, 
                    x="Year", 
                    y="Export_Amount", 
                    color="Continent of the territory", 
                    markers=True, 
                    title="Export Trend by Year and Region")
fig_trend.update_layout(
    width=1280,  # Adjust width
    height=600,  # Adjust height
    title_font_size=20
)

fig_trend.update_xaxes(
    dtick=1,  # Show every year
    tickmode="linear",
    title_text="Year",
    tickangle=90
)

st.plotly_chart(fig_trend)
