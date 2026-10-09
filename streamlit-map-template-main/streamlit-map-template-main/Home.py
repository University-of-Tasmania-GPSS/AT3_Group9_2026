
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

from pathlib import Path 
#Home.py is inside the inner project folder. 
# # Move up to the outer project folder. 
project_folder = Path(__file__).resolve().parents[1] 
data_folder = project_folder / "data" 
shapefile_path = ( data_folder / "SydneyLGAs_GetisOrd.shp" ) 
st.write("Project folder:", str(project_folder)) 
st.write("Data folder exists:", data_folder.exists()) 
st.write("Shapefile path:", str(shapefile_path)) 
st.write("Shapefile exists:", shapefile_path.exists()) 
# Check the shapefile's required component files 
for extension in [".shp", ".shx", ".dbf", ".prj"]: 
    component = shapefile_path.with_suffix(extension) 
    st.write( f"{extension} file exists:", component.exists() ) 
    
if not shapefile_path.exists(): 
        
    st.error("The shapefile could not be found.") 
    st.stop() 

try: 
    lga_shapefile = gpd.read_file(shapefile_path) 
    lga_shapefile = lga_shapefile.to_crs(epsg=4326) 
            
    st.success( f"Loaded {len(lga_shapefile)} LGA polygons." ) 
           
except Exception as e: 
    st.error(f"Shapefile loading failed: {e}") st.stop()





# project_folder = Path(__file__).resolve().parent.parent

# # Find the outer project's data folder 
# project_folder = Path(__file__).resolve().parents[2] 
# shapefile_path = ( project_folder / "data" / "SydneyLGAs_GetisOrd.shp" ) 

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
    { "name": "Drug Offences - total count", "field": "Drugs_Tota", "color": "#E3C441", },
    { "name": "Violent Crime - total count", "field": "VC_Total", "color": "#91AD59", },
    { "name": "Property Offences - total count", "field": "PO_Total", "color": "#34734A", },
    { "name": "Drug Offences — rate per 1,000", "field": "Drugs/1000", "color": "#E3C441", },
    { "name": "Violent Crime — rate per 1,000", "field": "VC/1000", "color": "#91AD59", },
    { "name": "Property Offences — rate per 1,000", "field": "PO/1000", "color": "#34734A", },
]

# Create Map
m = leafmap.Map( 
                center=(-33.87, 151.21), 
                zoom=9, 
                minimap_control=True, 
                draw_control=False, 
                measure_control=True, ) 

m.add_basemap("OpenStreetMap")


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
colours = [ "#ffffb2", "#fecc5c", "#fd8d3c", "#f03b20", "#bd0026", ] 

for layer in layers: 
    field = layer["field"] 
    
    if field not in lga_shapefile.columns: 
        st.warning(f"Missing field: {field}") 
        continue 
    
    layer_gdf = lga_shapefile[ ["LGA_NAME25", field, "geometry"] ].copy() 
    layer_gdf[field] = pd.to_numeric( layer_gdf[field], errors="coerce" ) 
    values = layer_gdf[field].dropna() 
    
    if values.empty: 
        st.warning(f"No data for {layer['name']}") 
        continue 

    breaks = values.quantile( [0, 0.2, 0.4, 0.6, 0.8, 1] ).tolist() 

    def style_function( feature, field=field, breaks=breaks, colours=colours, opacity=fill_opacity, ): 
        
        value = feature["properties"].get(field) 
        
        if value is None or pd.isna(value): 
            fill_colour = "#d9d9d9" 
        else: 
            class_index = sum( value > b for b in breaks[1:-1] ) 
            class_index = min(class_index, 4) 
            fill_colour = colours[class_index] 
            
        return { "fillColor": fill_colour, "color": "#555555", "weight": 1, "fillOpacity": opacity, "opacity": 0.8, } 
    
    m.add_gdf( layer_gdf, layer_name=layer["name"], style_function=style_function, info_mode="on_click", )

# Display map 


st.subheader("Interactive crime map") 
m.to_streamlit(height=700) 

st.caption( "Use the layer control on the map to toggle crime " "counts and rates. Click an LGA to inspect its attributes." )






# import streamlit as st
# import leafmap.foliumap as leafmap

# st.set_page_config(layout="wide")

# # Customize the sidebar
# markdown = """
# A Streamlit map template
# <https://github.com/opengeos/streamlit-map-template>
# """

# st.sidebar.title("About")
# st.sidebar.info(markdown)
# logo = "https://i.imgur.com/UbOXYAU.png"
# st.sidebar.image(logo)

# # Customize page title
# st.title("Streamlit for Geospatial Applications")

# st.markdown("""
#     This multipage app template demonstrates various interactive web apps created using [streamlit](https://streamlit.io) and [leafmap](https://leafmap.org). It is an open-source project and you are very welcome to contribute to the [GitHub repository](https://github.com/opengeos/streamlit-map-template).
#     """)

# st.header("Instructions")

# markdown = """
# 1. For the [GitHub repository](https://github.com/opengeos/streamlit-map-template) or [use it as a template](https://github.com/opengeos/streamlit-map-template/generate) for your own project.
# 2. Customize the sidebar by changing the sidebar text and logo in each Python files.
# 3. Find your favorite emoji from https://emojipedia.org.
# 4. Add a new app to the `pages/` directory with an emoji in the file name, e.g., `1_🚀_Chart.py`.

# """

# st.markdown(markdown)

# m = leafmap.Map(minimap_control=True)
# m.add_basemap("OpenTopoMap")
# m.to_streamlit(height=500)
