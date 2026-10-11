import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import pandas as pd

from pathlib import Path
from folium.plugins import MeasureControl


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Sydney Crime and Socioeconomic Map",
    page_icon="🌏",
    layout="wide",
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

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
            SYDNEY CRIME AND SOCIOECONOMIC MAP
        </p>
        <h1 style="color: white; margin: 0;">
            Mapping Crime and Socioeconomic Correlations
        </h1>
        <p style="
            color: #E5EDE7;
            font-size: 16px;
            margin-top: 10px;
            margin-bottom: 0;
        ">
            Explore the relationship between socioeconomic
            conditions and drug offences, violent crime and
            property offences across Greater Sydney LGAs.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# LOAD SHAPEFILE
# --------------------------------------------------

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

    # Convert to WGS84 for web mapping
    if lga_shapefile.crs is None:
        st.error(
            "The shapefile has no defined CRS. "
            "Set its correct source CRS before reprojecting."
        )
        st.stop()

    lga_shapefile = lga_shapefile.to_crs(
        epsg=4326
    )

except Exception as e:
    st.error(f"Shapefile loading failed: {e}")
    st.stop()


# --------------------------------------------------
# CONFIGURE THE THREE CORRELATION LAYERS
# --------------------------------------------------

layers = [
    {
        "name": "Drug offences — correlation",
        "field": "Drug_m",
        "significance": "sign_drug",
        "colour": "#2166AC",
    },
    {
        "name": "Violent crime — correlation",
        "field": "VC_m",
        "significance": "sign_VC",
        "colour": "#43956B",
    },
    {
        "name": "Property offences — correlation",
        "field": "PO_m",
        "significance": "sign_PO",
        "colour": "#8E63A9",
    },
]


# --------------------------------------------------
# CHECK REQUIRED FIELDS
# --------------------------------------------------

required_fields = [
    "Drug_m",
    "VC_m",
    "PO_m",
    "sign_drug",
    "sign_VC",
    "sign_PO",
]

missing_fields = [
    field
    for field in required_fields
    if field not in lga_shapefile.columns
]

if missing_fields:
    st.error(
        "The shapefile is missing these required columns: "
        + ", ".join(missing_fields)
    )
    st.stop()


# --------------------------------------------------
# MAP INTRODUCTION AND OPACITY CONTROL
# --------------------------------------------------

st.subheader("Interactive correlation map")

map_heading, opacity_column = st.columns(
    [3, 2],
    vertical_alignment="center",
)

with map_heading:
    st.caption(
        "Toggle the three crime layers using the map controls. "
        "Click an LGA to inspect its correlation coefficient "
        "and significance classification."
    )

with opacity_column:
    transparency = st.slider(
        "Polygon opacity (%)",
        min_value=0,
        max_value=100,
        value=70,
        step=5,
        help=(
            "Lower values make the polygons more transparent."
        ),
    )

fill_opacity = transparency / 100


# --------------------------------------------------
# COLOUR SCALE
# --------------------------------------------------

# Negative correlations: blue
# Near-zero correlations: white
# Positive correlations: red

colours = [
    "#2166AC",
    "#67A9CF",
    "#D1E5F0",
    "#F7F7F7",
    "#FDDBC7",
    "#EF8A62",
    "#B2182B",
]


def correlation_colour(value):
    """
    Map a correlation coefficient between -1 and +1
    onto a diverging colour scale.

    Assumes the stored values are correlation
    coefficients bounded by -1 and +1.
    """

    if pd.isna(value):
        return "#D9D9D9"

    value = max(-1.0, min(1.0, float(value)))

    # Seven equal-width intervals from -1 to +1
    index = min(
        int((value + 1) / 2 * len(colours)),
        len(colours) - 1,
    )

    return colours[index]


# --------------------------------------------------
# CREATE MAP
# --------------------------------------------------

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


# --------------------------------------------------
# FRIENDLY POPUP LABELS
# --------------------------------------------------

friendly_labels = {
    "LGA_NAME25": "Local Government Area",
    "Drug_m": "Drug offences - correlation value",
    "VC_m": "Violent crime - correlation value",
    "PO_m": "Property offences - correlation value",
    "sign_drug": "Drug offences - trend classification",
    "sign_VC": "Violent crime - trend classification",
    "sign_PO": "Property offences - trend classification",
}


# --------------------------------------------------
# ADD THE THREE TOGGLEABLE LAYERS
# --------------------------------------------------

for layer in layers:

    field = layer["field"]
    significance_field = layer["significance"]

    # Select the fields needed for this layer's popup
    layer_gdf = lga_shapefile[
        [
            "LGA_NAME25",
            field,
            significance_field,
            "geometry",
        ]
    ].copy()

    # Convert the gradient variable to numeric
    layer_gdf[field] = pd.to_numeric(
        layer_gdf[field],
        errors="coerce",
    )

    # Preserve the significance classification as text
    layer_gdf[significance_field] = (
        layer_gdf[significance_field]
        .astype("string")
    )

    # Rename the attributes for readable popups
    layer_gdf = layer_gdf.rename(
        columns=friendly_labels
    )

    display_field = friendly_labels[field]

    def style_function(
        feature,
        display_field=display_field,
        opacity=fill_opacity,
    ):
        value = feature["properties"].get(
            display_field
        )

        try:
            value = float(value)
        except (TypeError, ValueError):
            value = None

        if value is None or pd.isna(value):
            fill_colour = "#D9D9D9"
        else:
            fill_colour = correlation_colour(value)

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


# --------------------------------------------------
# DISPLAY MAP
# --------------------------------------------------

st.subheader("Explore socioeconomic correlations")

m.to_streamlit(height=700)

st.caption(
    "Toggle layers using the map's layer control. "
    "Click an LGA polygon to view its correlation "
    "coefficient and significance classification. "
    "Grey polygons indicate missing correlation values."
)


# --------------------------------------------------
# LEGEND
# --------------------------------------------------

st.subheader("Correlation coefficient legend")

legend_labels = [
    "Strong negative",
    "Moderate negative",
    "Weak negative",
    "Near zero",
    "Weak positive",
    "Moderate positive",
    "Strong positive",
]

legend_columns = st.columns(7)

for i, column in enumerate(legend_columns):
    with column:
        st.markdown(
            f"""
            <div style="
                background-color: {colours[i]};
                height: 18px;
                border-radius: 4px;
                margin-bottom: 5px;
                border: 1px solid #cccccc;
            "></div>
            <div style="
                font-size: 11px;
                text-align: center;
            ">{legend_labels[i]}</div>
            """,
            unsafe_allow_html=True,
        )

st.caption(
    "Blue indicates negative correlations, white indicates "
    "values near zero, and red indicates positive correlations. "
    "Grey indicates missing data. Interpret the coefficient "
    "according to the correlation method used in the analysis."
)


# --------------------------------------------------
# STUDY METADATA
# --------------------------------------------------

st.divider()

st.subheader("About this map")

with st.container(border=True):

    st.markdown("**Metadata**")

    meta_left, meta_right = st.columns(2)

    with meta_left:
        st.markdown(
            """
            **Geographic coverage:** Selected Greater Sydney LGAs

            **Study period:** 2015–2025

            **Mapped variables:** Drug offences, violent crime
            and property offences

            **Spatial unit:** Local Government Areas

            **Data source:** LGA boundaries and the associated
            socioeconomic and crime analysis dataset.
            """
        )

    with meta_right:
        st.markdown(
            """
            **Methodological notes:**

            - Each layer maps its stored correlation coefficient.
            - The significance classification is available
              in the clicked polygon's attributes.
            - Grey polygons indicate missing correlation values.
            - Correlation does not establish causation.
            - The interpretation of statistical significance
              depends on the method and threshold used in
              the underlying analysis.
            """
        )