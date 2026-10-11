import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import pandas as pd

from pathlib import Path
from folium.plugins import MeasureControl


# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Sydney Socioeconomic Correlation Map",
    page_icon="🌏",
    layout="wide",
)


# ==================================================
# 2. PAGE HEADER
# ==================================================

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
            SYDNEY SOCIOECONOMIC CORRELATION MAP | 2015–2025
        </p>
        <h1 style="color: white; margin: 0;">
            Mapping Crime and Socioeconomic Relationships
        </h1>
        <p style="
            color: #E5EDE7;
            font-size: 16px;
            margin-top: 10px;
            margin-bottom: 0;
        ">
            Explore how socioeconomic factors relate to drug
            offences, violent crime and property offences across
            selected Local Government Areas in Greater Sydney.
            Toggle the layers and click an LGA to inspect its values.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# 3. LOAD SHAPEFILE
# ==================================================

project_folder = Path(__file__).resolve().parents[1]
data_folder = project_folder / "data"

shapefile_path = (
    data_folder
    / "withchange_SydneyLGAs_MGA202056_socioecon_crime_2015_2025.shp"
)

if not shapefile_path.exists():
    st.error(
        f"Shapefile not found: {shapefile_path}"
    )
    st.stop()

try:
    lga_shapefile = gpd.read_file(shapefile_path)

    if lga_shapefile.crs is None:
        st.error(
            "The shapefile has no defined coordinate reference "
            "system (CRS). Please define its correct source CRS."
        )
        st.stop()

    # Reproject to WGS84 for web mapping
    lga_shapefile = lga_shapefile.to_crs(epsg=4326)

except Exception as e:
    st.error(f"Shapefile loading failed: {e}")
    st.stop()


# ==================================================
# 4. DEFINE THE THREE MAP LAYERS
# ==================================================

layers = [
    {
        "name": "Drug offences — socioeconomic correlation",
        "field": "Drug_m",
        "significance": "sign_drug",
    },
    {
        "name": "Violent crime — socioeconomic correlation",
        "field": "VC_m",
        "significance": "sign_vc",
    },
    {
        "name": "Property offences — socioeconomic correlation",
        "field": "PO_m",
        "significance": "sign_po",
    },
]


# ==================================================
# 5. CHECK REQUIRED COLUMNS
# ==================================================

required_fields = [
    "LGA_NAME25",
    "Drug_m",
    "VC_m",
    "PO_m",
    "sign_drug",
    "sign_vc",
    "sign_po",
]

missing_fields = [
    field
    for field in required_fields
    if field not in lga_shapefile.columns
]

if missing_fields:
    st.error(
        "The shapefile is missing these columns: "
        + ", ".join(missing_fields)
    )

    st.write(
        "Available columns:",
        lga_shapefile.columns.tolist(),
    )

    st.stop()


# ==================================================
# 6. MAP INTRODUCTION AND OPACITY SLIDER
# ==================================================

st.subheader("Interactive socioeconomic correlation map")

map_heading, opacity_column = st.columns(
    [3, 2],
    vertical_alignment="center",
)

with map_heading:
    st.caption(
        "Use the layer control to switch between drug offences, "
        "violent crime and property offences. Polygon colours "
        "show the correlation classification over time. "
        "Click an LGA to inspect its numerical correlation value."
    )

with opacity_column:
    transparency = st.slider(
        "Polygon opacity (%)",
        min_value=0,
        max_value=100,
        value=80,
        step=5,
        help=(
            "Lower values make the polygons more transparent."
        ),
    )

fill_opacity = transparency / 100


# ==================================================
# 7. DEFINE THE THREE COLOURS
# ==================================================

SIGN_COLOURS = {
    "positive": "#D73027",  # Red
    "none": "#FFFFFF",      # White
    "negative": "#4575B4",  # Blue
    "missing": "#D9D9D9",   # Grey for missing/unrecognised data
}


def classify_correlation(value):
    """Match the exact trend labels stored in the shapefile."""

    if value is None or pd.isna(value):
        return "missing"

    value = str(value).strip().lower()

    if value == "increasing over time":
        return "positive"

    elif value == "decreasing over time":
        return "negative"

    elif value == "no correlation over time":
        return "none"

    else:
        return "missing"


# ==================================================
# 8. CREATE THE MAP
# ==================================================

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


# ==================================================
# 9. FRIENDLY LABELS FOR CLICK POPUPS
# ==================================================

friendly_labels = {
    "LGA_NAME25": "Local Government Area",
    "Drug_m": "Drug offences - gradient value",
    "VC_m": "Violent crime - gradient value",
    "PO_m": "Property offences - gradient value",
    "sign_drug": "Drug offences - trend classification",
    "sign_vc": "Violent crime - trend classification",
    "sign_po": "Property offences - trend classification",
}


# ==================================================
# 10. ADD THE THREE TOGGLEABLE LAYERS
# ==================================================

for layer in layers:

    field = layer["field"]
    sign_field = layer["significance"]

    # Keep the numeric value and its matching classification
    layer_gdf = lga_shapefile[
        [
            "LGA_NAME25",
            field,
            sign_field,
            "geometry",
        ]
    ].copy()

    # Ensure the actual correlation value is numeric
    layer_gdf[field] = pd.to_numeric(
        layer_gdf[field],
        errors="coerce",
    )

    # Rename fields for readable click popups
    layer_gdf = layer_gdf.rename(
        columns=friendly_labels
    )

    display_sign = friendly_labels[sign_field]

    def style_function(
        feature,
        display_sign=display_sign,
        opacity=fill_opacity,
    ):
        # Classification determines the polygon colour
        sign_value = feature["properties"].get(
            display_sign
        )

        category = classify_correlation(sign_value)
        fill_colour = SIGN_COLOURS[category]

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


# ==================================================
# 11. DISPLAY THE MAP
# ==================================================

st.subheader("Explore correlations across Greater Sydney")

m.to_streamlit(height=700)

st.caption(
    "Toggle the three layers using the map's layer control. "
    "Click an LGA polygon to view the corresponding numerical "
    "correlation value and classification."
)


# ==================================================
# 12. THREE-COLOUR LEGEND
# ==================================================

st.subheader("Legend")

legend_items = [
    (SIGN_COLOURS["positive"], "Increasing over Time"),
    (SIGN_COLOURS["none"], "No correlation over Time"),
    (SIGN_COLOURS["negative"], "Decreasing correlation over Time"),
]

legend_columns = st.columns(3)

for i, (colour, label) in enumerate(legend_items):
    with legend_columns[i]:
        st.markdown(
            f"""
            <div style="
                background-color: {colour};
                height: 24px;
                border: 1px solid #777777;
                border-radius: 4px;
                margin-bottom: 6px;
            "></div>
            <div style="
                font-size: 13px;
                text-align: center;
            ">{label}</div>
            """,
            unsafe_allow_html=True,
        )

st.caption(
    "Red represents increasing gradient, white represents "
    "no correlation, and blue represents decreasing gradient. "
    "Grey indicates missing or unrecognised classification data. "
    "Numerical values are available by clicking an LGA."
)


# ==================================================
# 13. STUDY METADATA
# ==================================================

st.divider()

st.subheader("About this map")

with st.container(border=True):

    st.markdown("**Metadata**")

    meta_left, meta_right = st.columns(2)

    with meta_left:
        st.markdown(
            """
            **Study period:** January 2015 - December 2025

            **Coordinate System:** GDA2020 / MGA Zone 56 (EPSG:7856); reprojected to WGS84 (EPSG:4326) for web mapping.

            **Study area:** Selected Greater Sydney Local Government Areas
            
            **Crime categories:** Drug offences, violent crime and property offences

            **Mapped variables:** Drug offences, violent crime
            and property offences.
            
            **Data Source:** LGA polygons, Australian Bureau of Statistics Local Government Area boundaries (2025). 
            Crime data, NSW Bureau of Crime Statistics and Research, Recorded Criminal incidents by month by LGA. 
            Socioeconomic data, Australian Bureau of Statistics, 2021. Data cleaning conducted by T. Powell, 2026. 
            Gradient calculation and classification for each LGA conducted by T.Powell, 2026.

            **Map Producer:** Molly Marshall, 2026
                                            
            **Date:** 11 October 2026

            """
        )
        

    with meta_right:
        st.markdown(
            """
            **Methodological notes:**

            - Polygon colours are determined by the relevant
              classification field: `sign_drug`, `sign_vc`
              or `sign_po`.
            - Numerical correlation values are stored in
              `Drug_m`, `VC_m` and `PO_m` and are displayed
              when a polygon is clicked.
            - Grey polygons indicate missing or unrecognised
              classification values.
            - Correlation does not establish causation.
            - Interpretation depends on the methodology used
              to calculate the underlying correlations.
            """
        )

   