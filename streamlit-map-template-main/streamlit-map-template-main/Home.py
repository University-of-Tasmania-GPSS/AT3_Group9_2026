
import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd 
from pathlib import Path
import pandas as pd
from folium.plugins import MeasureControl

st.set_page_config(page_title="Sydney Crime Explorer Map", page_icon = "🌏", layout="wide")

# Title and into

st.markdown(
    """
    <div style="
        background-color: #244B36;
        padding: 26px 30px;
        border-radius: 10px;
        margin-bottom: 18px;
    ">
        <p style="
            color: #F4D35E;
            font-size: 12px;
            font-weight: bold;
            letter-spacing: 2px;
            margin-bottom: 8px;
        ">
            SYDNEY CRIME EXPLORER MAP | 2015–2025
        </p>
        <h1 style="color: white; margin: 0;">
            Mapping Crime Across Greater Sydney
        </h1>
        <p style="
            color: #E5EDE7;
            font-size: 16px;
            margin-top: 10px;
            margin-bottom: 0;
        ">
            Explore the spatial distribution of drug offences,
            violent crime and property offences across selected
            Local Government Areas in Greater Sydney, Australia.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# load shapefile 
# Load shapefile from your GitHub repository
project_folder = Path(__file__).resolve().parents[1] 
data_folder = project_folder / "data" 
shapefile_path = ( data_folder / "SydneyLGAs_GetisOrd.shp" ) 

# Check the shapefile's required component files 
for extension in [".shp", ".shx", ".dbf", ".prj"]: 
    component = shapefile_path.with_suffix(extension) 
    
if not shapefile_path.exists(): 
    st.error("The shapefile could not be found.") 
    st.stop() 

try: 
    lga_shapefile = gpd.read_file(shapefile_path) 
    lga_shapefile = lga_shapefile.to_crs(epsg=4326) 
           
except Exception as e: 
    st.error(f"Shapefile loading failed: {e}") 
    st.stop()

lga_shapefile = gpd.read_file(shapefile_path) 

# Convert to WGS84 for web mapping 
lga_shapefile = lga_shapefile.to_crs(epsg=4326)

# Define 6 map layers 

layers = [
    { "name": "Drug Offences - total count", "field": "Drugs_Tota", "color": "#E3C441", },
    { "name": "Violent Crime - total count", "field": "VC_Total", "color": "#91AD59", },
    { "name": "Property Offences - total count", "field": "PO_Total", "color": "#34734A", },
    { "name": "Drug Offences - rate per 1,000", "field": "Drugs/1000", "color": "#E3C441", },
    { "name": "Violent Crime - rate per 1,000", "field": "VC/1000", "color": "#91AD59", },
    { "name": "Property Offences - rate per 1,000", "field": "PO/1000", "color": "#34734A", },
]

# Map header

# Low to high: yellow, orange, red
colours = [
    "#ffffb2",
    "#fecc5c",
    "#fd8d3c",
    "#f03b20",
    "#bd0026",
]

st.subheader("Interactive crime map")

map_heading, opacity_column = st.columns(
    [3, 2],
    vertical_alignment="center",
)

with map_heading:
    st.caption(
        "Toggle layers using the map's layer control. This web map presents the spatial distribution of recorded count and rate per 1000 people of criminal incidents across selected Greater Sydney Local Government Areas (LGAs) over the period January 2015 to December 2025."
    )

with opacity_column:
    transparency = st.slider(
        "Polygon opacity (%)",
        min_value=0,
        max_value=100,
        value=70,
        step=5,
        help=(
            "Lower values make the polygons more "
            "transparent so the basemap is visible."
        ),
    )

fill_opacity = transparency / 100


# Create Map
m = leafmap.Map(
    center=(-33.87, 151.21),
    zoom=9,
    minimap_control=True,
    draw_control=False,
    measure_control=False,
)

m.add_basemap("OpenStreetMap")

m.add_child(
    MeasureControl(
        primary_length_unit="meters",
        secondary_length_unit="kilometers",
        primary_area_unit="sqmeters",
        secondary_area_unit="hectares",
    )
)


colours = [
    "#ffffb2",
    "#fecc5c",
    "#fd8d3c",
    "#f03b20",
    "#bd0026",
]

# Friendly labels for the click pop-ups
friendly_labels = {
    "LGA_NAME25": "Local Government Area",
    "Drugs_Tota": "Total drug offences (2015–2025)",
    "VC_Total": "Total violent crime incidents (2015–2025)",
    "PO_Total": "Total property offences (2015–2025)",
    "Drugs/1000": "Drug offences per 1,000 residents",
    "VC/1000": "Violent crime per 1,000 residents",
    "PO/1000": "Property offences per 1,000 residents",
}

for layer in layers:
    field = layer["field"]

    if field not in lga_shapefile.columns:
        st.warning(f"Missing field: {field}")
        continue

    # Keep the original field names temporarily
    layer_gdf = lga_shapefile[
        ["LGA_NAME25", field, "geometry"]
    ].copy()

    # Rename fields for the map display
    layer_gdf = layer_gdf.rename(
        columns=friendly_labels
    )

    # The friendly name for the selected crime variable
    display_field = friendly_labels[field]

    # Convert crime values to numbers
    layer_gdf[display_field] = pd.to_numeric(
        layer_gdf[display_field],
        errors="coerce",
    )

    # Calculate quantile classes using the renamed field
    values = layer_gdf[display_field].dropna()

    if values.empty:
        st.warning(f"No data for {layer['name']}")
        continue

    breaks = values.quantile(
        [0, 0.2, 0.4, 0.6, 0.8, 1]
    ).tolist()

    def style_function(
        feature,
        display_field=display_field,
        breaks=breaks,
        colours=colours,
        opacity=fill_opacity,
    ):
        value = feature["properties"].get(display_field)

        if value is None or pd.isna(value):
            fill_colour = "#d9d9d9"
        else:
            class_index = sum(
                value > b for b in breaks[1:-1]
            )
            class_index = min(class_index, 4)
            fill_colour = colours[class_index]

        return {
            "fillColor": fill_colour,
            "color": "#555555",
            "weight": 1,
            "fillOpacity": opacity,
            "opacity": 0.8,
        }

    m.add_gdf(
        layer_gdf,
        layer_name=layer["name"],
        style_function=style_function,
        info_mode="on_click",
    )

# Display map 
st.subheader("Interactive map of crime counts and rates") 
m.to_streamlit(height=700) 

st.caption( "Use the layer control on the map to toggle crime " "counts and rates. Click an LGA to inspect its attributes." )


# Colour legend
st.subheader("Legend")
st.markdown("**Crime Count/Rate**")

legend_columns = st.columns(5)

legend_labels = [
    "Very Low",
    "Low",
    "Moderate",
    "High",
    "Very High",
]

for i, column in enumerate(legend_columns):
    with column:
        st.markdown(
            f"""
            <div style="
                background-color: {colours[i]};
                height: 16px;
                border-radius: 4px;
                margin-bottom: 5px;
            "></div>
            <div style="
                font-size: 12px;
                text-align: center;
            ">{legend_labels[i]}</div>
            """,
            unsafe_allow_html=True,
        )

st.caption(
    "Colours represent relative quantile classes within "
    "each selected layer. Yellow indicates lower values "
    "and dark red indicates higher values. Grey indicates "
    "missing data. Class boundaries can differ between "
    "crime counts and crime rates."
)


# STUDY METADATA

st.divider()

st.subheader("About this Map")

with st.container(border=True):
    st.markdown("**Metadata**")

    meta_left, meta_right = st.columns(2)

    with meta_left:
        st.markdown(
            """
            **Study period:** January 2015 - December 2025

            **Coordinate System:** GDA2020 / MGA Zone 56 (EPSG:7856); reprojected to WGS84 (EPSG:4326) for web mapping.

            **Crime Groups:** Drug offences, violent crime and property offences
            
            **Data Source:** LGA polygons, Australian Bureau of Statistics
            Local Government Area boundaries (2025). Crime data, NSW Bureau of Crime Statistics and Research, 
            Recorded Criminal incidents by month by LGA. Data cleaning conducted by T. Powell, 2026. Crime count and 
            rate computed by M.Marshall, 2026.
            
            **Map Producer:** Molly Marshall, 2026
            
            **Date:** 9 October 2026
            """
        )

    with meta_right:
        st.markdown(
            """
            **Methodological notes:**
              - Crime counts represent the sum of recorded incidents
                  across 2015–2025.
                - Crime rates are calculated as total recorded incidents
                  divided by the relevant population, multiplied by 1,000.
                - The graduated colour scale uses five quantile classes.
                  Class boundaries are calculated separately for each
                  crime variable.
                - Recorded incidents describe offences known to police
                  and do not necessarily represent all crime that occurs.
            """
        )



