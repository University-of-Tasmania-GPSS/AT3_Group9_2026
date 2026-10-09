
import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd 
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="Sydney Crime Explorer Map", layout="wide")


#side bar
    

st.sidebar.title("About this map")
st.sidebar.info("""**Study period:** January 2015 – December 2025 **Study area:** Selected Sydney LGAs **Data:** NSW Bureau of Crime Statistics and Research and Australian Bureau of Statistics. **Map theme:** Green and yellow """ )


st.title("Interactive Map")
 
# load shapefile 
# Load shapefile from your GitHub repository
project_folder = Path(__file__).resolve().parent.parent

# Find the outer project's data folder 
project_folder = Path(__file__).resolve().parents[2] 
shapefile_path = ( project_folder / "data" / "SydneyLGAs_GetisOrd.shp" ) 

st.write("Shapefile path:", str(shapefile_path)) 
st.write("File exists:", shapefile_path.exists()) 
lga_shapefile = gpd.read_file(shapefile_path) 

# Convert to WGS84 for web mapping 
lga_shapefile = lga_shapefile.to_crs(epsg=4326)

# page title
st.title("Sydney Crime Explorer Map")
st.markdown("""Explore recorded crime across Greater Sydney's Local Government Areas (LGAs).
    Use the layer control in the top-right corner of the map
    to switch between crime counts and crime rates.
    Click a polygon to view its statistics.
    """)

# define 6 map layers 

layers = [
    { "name": "Drug crime — total count", "field": "Drugs_Tota", "color": "#E3C441", },
    { "name": "Violent crime — total count", "field": "VC_Total", "color": "#91AD59", },
    { "name": "Property crime — total count", "field": "PO_Total", "color": "#34734A", },
    { "name": "Drug crime — rate per 1,000", "field": "Drugs/1000", "color": "#E3C441", },
    { "name": "Violent crime — rate per 1,000", "field": "VC/1000", "color": "#91AD59", },
    { "name": "Property crime — rate per 1,000", "field": "PO/1000", "color": "#34734A", },
]

# Create Map
m = leafmap.Map( 
                center=(-33.87, 151.21), 
                zoom=9, 
                minimap_control=True, 
                draw_control=False, 
                measure_control=True, ) 

m.add_basemap("OpenTopoMap")


st.sidebar.subheader("Map appearance")

transparency = st.sidebar.slider(
    "Polygon opacity",
    min_value=0,
    max_value=100,
    value=40,
    step=5,
)

fill_opacity = transparency / 100


# add polygon layers 
# Green-to-yellow colour scale: low to high 
colours = [ "#ffffcc", # Very low - pale yellow 
           "#c2e699", # Low 
           "#78c679", # Moderate 
           "#31a354", # High 
           "#006837", # Very high - dark green 
] 
        
for layer in layers: 
    field = layer["field"] 
    
    # Check the field exists 
    if field not in lga_shapefile.columns: 
        st.warning( f"Skipping {layer['name']}: " 
                   f"field '{field}' was not found." 
        ) 
        continue 
    
    # Keep only the columns needed for this layer 
    layer_gdf = lga_shapefile[ ["LGA_NAME25", field, "geometry"] ].copy() 
    
    # Convert the field to numeric values 
    layer_gdf[field] = pd.to_numeric( layer_gdf[field], errors="coerce" ) 
    
    # Calculate the quantile breaks for this layer 
    values = layer_gdf[field].dropna() 
    
    if values.empty: 
        st.warning(f"No valid data for {layer['name']}") 
        continue 
breaks = values.quantile( [0, 0.2, 0.4, 0.6, 0.8, 1] ).tolist() 

# Style each LGA according to its crime value 
def style_function( feature, field=field, breaks=breaks, colours=colours, opacity=fill_opacity, ): 
    value = feature["properties"].get(field) 
    # Show missing data in grey 
    if value is None or pd.isna(value): 
        fill_colour = "#d9d9d9" 
    
    else: 
        # Default to the highest colour 
        fill_colour = colours[-1] 
        
        # Assign the colour based on quantile class 
        for i in range(1, len(breaks)): 
            if value <= breaks[i]: fill_colour = colours[i - 1] 
            break 
        
        return { "fillColor": fill_colour, "color": "#465746", "weight": 0.8, "fillOpacity": opacity, "opacity": 0.8, } 
    
    # Add this layer to the map 
    m.add_gdf( layer_gdf, layer_name=layer["name"], style_function=style_function, info_mode="on_click", )

# Display map 


st.subheader("Interactive crime map") 
m.to_streamlit(height=700) 

st.caption( "Use the layer control on the map to toggle crime " "counts and rates. Click an LGA to inspect its attributes." )


