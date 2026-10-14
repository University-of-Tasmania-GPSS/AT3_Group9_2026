import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import pandas as pd

from pathlib import Path
from folium.plugins import MeasureControl


# 1. PAGE CONFIGURATION

st.set_page_config(
    page_title="Sydney Crime Trends Map",
    page_icon="🌏",
    layout="wide",
)


# 2. PAGE HEADER

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
            SYDNEY CRIME TRENDS | 2015–2025
        </p>
        <h1 style="color: white; margin: 0;">
            Mapping Crime Trends Across Greater Sydney
        </h1>
        <p style="
            color: #E5EDE7;
            font-size: 16px;
            margin-top: 10px;
            margin-bottom: 0;
        ">
            Explore how drug offences, violent crime and property
            offences have changed over time across selected
            Local Government Areas in Greater Sydney, Australia.
            Click an LGA to inspect crime trends and socioeconomic
            characteristics.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# 3. LOAD SHAPEFILE

project_folder = Path(__file__).resolve().parents[1]
data_folder = project_folder / "data"

shapefile_path = (
    data_folder
    / "withchange_SydneyLGAs_MGA202056_socioecon_crime_2015_2025.shp"
)

if not shapefile_path.exists():
    st.error(f"Shapefile not found: {shapefile_path}")
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


# 4. DEFINE THE THREE MAP LAYERS

layers = [
    {
        "name": "Drug offences - change over time",
        "field": "Drug_m",
        "classification": "sign_drug",
    },
    {
        "name": "Violent crime - change over time",
        "field": "VC_m",
        "classification": "sign_vc",
    },
    {
        "name": "Property offences - change over time",
        "field": "PO_m",
        "classification": "sign_po",
    },
]

# 5. CHECK REQUIRED COLUMNS

required_fields = [
    "LGA_NAME25",
    "Drug_m",
    "VC_m",
    "PO_m",
    "sign_drug",
    "sign_vc",
    "sign_po",
    "Median_tot",
    "High_Schoo",
    "Unemployme",
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
        "Available shapefile columns:",
        lga_shapefile.columns.tolist(),
    )

    st.stop()


# 6. MAP INTRODUCTION AND OPACITY SLIDER

st.subheader("Interactive crime trends map")

map_heading, opacity_column = st.columns(
    [3, 2],
    vertical_alignment="center",
)

with map_heading:
    st.caption(
        "Explore recorded crime trends across Greater Sydney "
        "LGAs from 2015 to 2025. Toggle the three crime layers "
        "and click an LGA to inspect its crime trend value, "
        "trend classification and socioeconomic characteristics."
    )

with opacity_column:
    transparency = st.slider(
        "Polygon opacity (%)",
        min_value=0,
        max_value=100,
        value=80,
        step=5,
        help=(
            "Lower values make the polygons more transparent "
            "so the basemap is easier to see."
        ),
    )

fill_opacity = transparency / 100


# 7. DEFINE COLOURS AND CLASSIFICATIONS

SIGN_COLOURS = {
    "increasing": "#D73027",       # Red
    "no_correlation": "#FFFFFF",   # White
    "decreasing": "#4575B4",       # Blue
    "missing": "#D9D9D9",          # Grey
}


def classify_trend(value):
    """Match the trend classifications stored in the shapefile."""

    if value is None or pd.isna(value):
        return "missing"

    value = str(value).strip().lower()

    if value == "increasing over time":
        return "increasing"

    elif value == "no correlation over time":
        return "no_correlation"

    elif value == "decreasing over time":
        return "decreasing"

    else:
        return "missing"


# 8. CREATE THE MAP

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


# 9. FRIENDLY LABELS FOR CLICK POPUPS

friendly_labels = {
    "LGA_NAME25": "Local Government Area",

    # Crime trend values
    "Drug_m": "Drug offences - numerical trend value",
    "VC_m": "Violent crime - numerical trend value",
    "PO_m": "Property offences - numerical trend value",

    # Crime trend classifications
    "sign_drug": "Drug offences - trend classification",
    "sign_vc": "Violent crime - trend classification",
    "sign_po": "Property offences - trend classification",

    # Socioeconomic characteristics
    "Median_tot": "Median total income",
    "High_Schoo": "High school percentage rate",
    "Unemployme": "Unemployment percentage rate",
}


# 10. ADD THE THREE TOGGLEABLE LAYERS


for layer in layers:

    field = layer["field"]
    classification_field = layer["classification"]

    # Include the relevant crime variables and all three
    # socioeconomic variables in every layer's popup.
    selected_fields = [
        "LGA_NAME25",
        field,
        classification_field,
        "Median_tot",
        "High_Schoo",
        "Unemployme",
        "geometry",
    ]

    layer_gdf = lga_shapefile[selected_fields].copy()

    # Convert numeric fields to numbers where possible.
    numeric_fields = [
        field,
        "Median_tot",
        "High_Schoo",
        "Unemployme",
    ]

    for numeric_field in numeric_fields:
        layer_gdf[numeric_field] = pd.to_numeric(
            layer_gdf[numeric_field],
            errors="coerce",
        )

    # Rename columns for readable click popups.
    layer_gdf = layer_gdf.rename(
        columns=friendly_labels
    )

    display_classification = friendly_labels[
        classification_field
    ]

    def style_function(
        feature,
        display_classification=display_classification,
        opacity=fill_opacity,
    ):
        # Use the classification field to determine the colour.
        trend_value = feature["properties"].get(
            display_classification
        )

        trend_category = classify_trend(trend_value)
        fill_colour = SIGN_COLOURS[trend_category]

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


# 11. DISPLAY THE MAP


st.subheader("Explore crime trends across Greater Sydney")

m.to_streamlit(height=700)

st.caption(
    "Toggle drug offences, violent crime or property offences "
    "using the map layer control. Click an LGA polygon to see "
    "its crime trend value, classification, median total income, "
    "high school percentage rate and unemployment percentage rate."
)


# 12. THREE-COLOUR LEGEND


st.subheader("Legend")

legend_items = [
    (SIGN_COLOURS["increasing"], "Increasing over Time"),
    (SIGN_COLOURS["no_correlation"], "No Correlation over Time"),
    (SIGN_COLOURS["decreasing"], "Decreasing over Time"),
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
    "Red indicates an increasing crime trend, white indicates "
    "no correlation over time, and blue indicates a decreasing "
    "crime trend. Grey indicates missing or unrecognised "
    "classification data."
)


# 13. STUDY METADATA

st.divider()

st.subheader("About this map")

with st.container(border=True):

    st.markdown("**Metadata**")

    meta_left, meta_right = st.columns(2)

    with meta_left:
        st.markdown(
            """
            **Study period:** January 2015 – December 2025

            **Coordinate system:** GDA2020 / MGA Zone 56
            (EPSG:7856), reprojected to WGS84 (EPSG:4326)
            for web mapping.

            **Study area:** Selected Greater Sydney
            Local Government Areas.

            **Crime categories:** Drug offences, violent crime
            and property offences.

            **Socioeconomic indicators:** Median total income,
            high school percentage rate and unemployment
            percentage rate.

            **Data sources:** Australian Bureau of Statistics
            Local Government Area boundaries (2025); NSW Bureau
            of Crime Statistics and Research recorded criminal
            incidents by month and LGA; socioeconomic data
            collated from the Australian Bureau of Statistics 2021 Census Data.

            **Data processing:** Data cleaning, crime trend
            value calculation and classification conducted by
            T. Powell, 2026. Crime rate computed by M. Marshall, 2026.

            **Map producer:** Molly Marshall, 2026.

            **Date:** 11 October 2026.
            """
        )

    with meta_right:
        st.markdown(
            """
            **Methodological notes:**

            - Each layer displays the temporal trend
              classification for one crime category in each LGA.
            - Red represents increasing trends, white represents
              no correlation over time, and blue represents
              decreasing trends.
            - Classifications are determined by `sign_drug`,
              `sign_vc` and `sign_po`.
            - Crime trend values are stored in `Drug_m`,
              `VC_m` and `PO_m`.
            - Clicking an LGA also displays median total income,
              high school percentage rate and unemployment
              percentage rate.
            - Grey polygons indicate missing or unrecognised
              classification values.
            - Recorded incidents represent offences known to
              police and may not reflect all crime that occurs.
            - Displaying socioeconomic indicators alongside
              crime trends does not establish a causal relationship.
            """
        )












