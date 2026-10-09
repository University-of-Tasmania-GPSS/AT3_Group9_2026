
import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd 
import pathlib as Path

st.set_page_config(page_title="Sydney Crime Explorer Map", layout="wide")

#side bar
    

st.sidebar.title("About this map")
st.sidebar.info("""**Study period:** January 2015 – December 2025 **Study area:** Selected Sydney LGAs **Data:** NSW Bureau of Crime Statistics and Research and Australian Bureau of Statistics. **Map theme:** Green and yellow """ )


st.title("Interactive Map")

# load shapefile 
# Load shapefile from your GitHub repository
shapefile_path = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "SydneyLGAs_MGA202056_socioecon_crime_2015_2025.shp"
)
lga_shapefile = gpd.read_file(shapefile_path / "SydneyLGAs_MGA202056_socioecon_crime_2015_2025.shp")
lga_shapefile = lga_shapefile.to_crs(epsg=4326)  # Convert to WGS84 for mapping

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


# add polygon layers 
for layer in layers: 
    field = layer["field"] 
    
    if field not in gdf.columns: 
        st.warning( f"Skipping {layer['name']}: " 
                   f"field '{field}' was not found." ) 
        continue 
    
    # Use a separate GeoDataFrame for each layer 
    layer_gdf = gdf[ 
                    ["LGA_NAME25", field, "geometry"] 
    ].copy() 
    
    layer_gdf[field] = ( 
                        layer_gdf[field].fillna(0) ) 
    
    # Graduated fill colour based on the selected field 
    values = layer_gdf[field] 
    minimum = values.min() 
    maximum = values.max() 
    
    if minimum == maximum: 
        midpoint = minimum 
        
    else: midpoint = (minimum + maximum) / 2 
    
    def style_function(feature, field=field, color=layer["color"], midpoint=midpoint, maximum=maximum): 
        
        value = feature["properties"].get(field, 0) 
    
        if value is None: 
            value = 0 
        
        if value <= midpoint: 
            fill_opacity = 0.35 
        else: 
            fill_opacity = 0.75 
    
        return { "fillColor": color, "color": "#465746", "weight": 0.8, "fillOpacity": fill_opacity, } 

m.add_gdf( layer_gdf, layer_name=layer["name"], style_function=style_function, info_mode="on_click", )

# Display map 


st.subheader("Interactive crime map") 
m.to_streamlit(height=700) 

st.caption( "Use the layer control on the map to toggle crime " "counts and rates. Click an LGA to inspect its attributes." )


