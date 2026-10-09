import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import pandas as pd
from pathlib import Path
from folium.plugins import MeasureControl

st.set_page_config(
    page_title="Sydney Crime Hotspot Map",
    page_icon="🌏",
    layout="wide",
)


# 1. PAGE TITLE

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
            SYDNEY CRIME HOTSPOT ANALYSIS | 2015–2025
        </p>
        <h1 style="color: white; margin: 0;">
            Mapping Crime Hotspots Across Greater Sydney
        </h1>
        <p style="
            color: #E5EDE7;
            font-size: 16px;
            margin-top: 10px;
            margin-bottom: 0;
        ">
            Explore statistically significant clusters of high
            and low crime rates across selected Greater Sydney
            Local Government Areas.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# 2. LOAD SHAPEFILE

project_folder = Path(__file__).resolve().parents[1]
data_folder = project_folder / "data"

shapefile_path = data_folder / "SydneyLGAs_GetisOrd.shp"

if not shapefile_path.exists():
    st.error(
        f"Shapefile not found: {shapefile_path}. "
        "Check the project folder and data directory."
    )
    st.stop()

try:
    lga_shapefile = gpd.read_file(shapefile_path)

    if lga_shapefile.crs is None:
        st.error(
            "The shapefile has no defined coordinate "
            "reference system (CRS)."
        )
        st.stop()

    lga_shapefile = lga_shapefile.to_crs(epsg=4326)

except Exception as e:
    st.error(f"Could not load shapefile: {e}")
    st.stop()


# 3. DEFINE HOTSPOT LAYERS

layers = [
    {
        "name": "Drug Offence Hotspots",
        "category_field": "Drug_Gi_Ca",
        "z_field": "Drug_Z",
        "p_field": "Drug_P",
    },
    {
        "name": "Violent Crime Hotspots",
        "category_field": "VC_Gi_Cate",
        "z_field": "VC_Z",
        "p_field": "VC_P",
    },
    {
        "name": "Property Offence Hotspots",
        "category_field": "PO_Gi_Cate",
        "z_field": "PO_Z",
        "p_field": "PO_P",
    },
]

required_fields = [
    "LGA_NAME25",
    "Drug_Gi_Ca", "Drug_Z", "Drug_P",
    "VC_Gi_Cate", "VC_Z", "VC_P",
    "PO_Gi_Cate", "PO_Z", "PO_P",
]

missing_fields = [
    field for field in required_fields
    if field not in lga_shapefile.columns
]

if missing_fields:
    st.error(
        "The shapefile is missing these required fields: "
        + ", ".join(missing_fields)
    )
    st.stop()


# 4. MAP INTRODUCTION AND OPACITY CONTROL

st.subheader("Interactive crime hotspot map")

map_heading, opacity_column = st.columns(
    [3, 2],
    vertical_alignment="center",
)

with map_heading:
    st.caption(
        "Use the layer control in the top-right corner to "
        "switch between crime categories. Click an LGA to "
        "inspect its hotspot classification, Z-score and "
        "p-value for each type of crime."
    )

with opacity_column:
    transparency = st.slider(
        "Polygon opacity (%)",
        min_value=0,
        max_value=100,
        value=75,
        step=5,
        help="Reduce opacity to see more of the basemap.",
    )

fill_opacity = transparency / 100


# 5. DEFINE HOTSPOT COLOURS

category_colours = {
    "hotspot": "#D73027",
    "coldspot": "#4575B4",
    "not significant": "#D9D9D9",
}

def classify_category(value):
    """Match the category labels stored in the shapefile."""

    if value is None or pd.isna(value):
        return "not significant"

    value = str(value).strip().lower()

    if "hotspot" in value or "hot spot" in value:
        return "hotspot"

    if "coldspot" in value or "cold spot" in value:
        return "coldspot"

    return "not significant"


# 6. CREATE MAP

# m = leafmap.Map(
#     center=(-33.87, 151.21),
#     zoom=9,
#     minimap_control=True,
#     draw_control=False,
#     measure_control=True,
# )

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



# 7. ADD HOTSPOT LAYERS

for layer in layers:

    category_field = layer["category_field"]
    z_field = layer["z_field"]
    p_field = layer["p_field"]

    # Select only attributes required for this layer
    layer_gdf = lga_shapefile[
        [
            "LGA_NAME25",
            category_field,
            z_field,
            p_field,
            "geometry",
        ]
    ].copy()

    # Make popup labels more understandable
    layer_gdf = layer_gdf.rename(
        columns={
            "LGA_NAME25": "Local Government Area",
            category_field: "Hotspot classification",
            z_field: "Getis-Ord Gi* Z-score",
            p_field: "P-value",
        }
    )

    # Standardise the categories for map styling
    display_category = "Hotspot classification"

    layer_gdf[display_category] = (
        layer_gdf[display_category].apply(classify_category)
    )

    # Ensure statistics are numeric
    layer_gdf["Getis-Ord Gi* Z-score"] = pd.to_numeric(
        layer_gdf["Getis-Ord Gi* Z-score"],
        errors="coerce",
    )

    layer_gdf["P-value"] = pd.to_numeric(
        layer_gdf["P-value"],
        errors="coerce",
    )

    def style_function(
        feature,
        display_category=display_category,
        opacity=fill_opacity,
    ):
        category = feature["properties"].get(
            display_category,
            "not significant",
        )

        fill_colour = category_colours.get(
            category,
            "#D9D9D9",
        )

        return {
            "fillColor": fill_colour,
            "color": "#555555",
            "weight": 1,
            "fillOpacity": opacity,
            "opacity": 0.9,
        }

    m.add_gdf(
        layer_gdf,
        layer_name=layer["name"],
        style_function=style_function,
        info_mode="on_click",
    )


# 8. DISPLAY MAP

m.to_streamlit(height=700)

st.caption(
    "Toggle the three layers to compare the spatial patterns "
    "of drug, violent and property crime hotspots."
)


# 9. LEGEND

st.subheader("Map legend")

legend_items = [
    ("#D73027", "Hotspot", "High crime-rate clustering"),
    ("#4575B4", "Coldspot", "Low crime-rate clustering"),
    ("#D9D9D9", "Not significant", "No statistically significant cluster"),
]

legend_columns = st.columns(3)

for column, (colour, label, description) in zip(
    legend_columns, legend_items
):
    with column:
        st.markdown(
            f"""
            <div style="
                display: flex;
                align-items: center;
                gap: 10px;
                margin-bottom: 6px;
            ">
                <div style="
                    background-color: {colour};
                    width: 24px;
                    height: 24px;
                    border: 1px solid #777;
                    border-radius: 4px;
                    flex-shrink: 0;
                "></div>
                <strong>{label}</strong>
            </div>
            <div style="font-size: 13px; margin-left: 34px;">
                {description}
            </div>
            """,
            unsafe_allow_html=True,
        )

st.caption(
    "Red indicates a statistically significant cluster of "
    "high crime-rate values; blue indicates a cluster of low "
    "values. Grey represents areas without a significant "
    "hotspot or coldspot classification."
)


# 10. STUDY METADATA

st.divider()
st.subheader("About this map")

with st.container(border=True):

    meta_left, meta_right = st.columns(2)

    with meta_left:
        st.markdown(
            """
            **Study period:** January 2015 – December 2025
            
            **Coordinate System:** GDA2020 / MGA Zone 56 (EPSG:7856); reprojected to WGS84 (EPSG:4326) for web mapping.

            **Study area:** Selected Greater Sydney Local Government Areas

            **Crime categories:** Drug offences, violent crime and property offences
            
            **Data Source:** LGA polygons, Australian Bureau of Statistics Local Government Area boundaries (2025). 
            Crime data, NSW Bureau of Crime Statistics and Research, Recorded Criminal incidents by month by LGA. 
            Data cleaning conducted by T. Powell, 2026. Hotspot autocorrelation using Getis-Ord Gi* analysis 
            computed by M.Marshall, 2026.
            
            **Map Producer:** Molly Marshall, 2026
                                
            **Date:** 10 October 2026
            """
        )
        

    with meta_right:
        st.markdown(
            """
            **Methodological notes:**
            - Queen contiguity spatial weights were used to define neighbouring LGAs.
            - Statistical significance was assessed using 199 permutations and a threshold of p < 0.05.
            - Z-scores indicate whether local crime-rate values are unusually high or low relative to their spatial neighbourhood.
            - P-values indicate the statistical evidence against the spatial-randomness assumption.
            - A hotspot indicates a cluster of high values; a coldspot indicates a cluster of low values.
            - These are spatial associations and do not establish the causes of crime.
            """
        )



