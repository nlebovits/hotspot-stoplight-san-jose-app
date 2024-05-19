import glob
import os
import subprocess
import tempfile
import zipfile

import ee
import geemap
import geopandas as gpd
import streamlit as st
from google.cloud import storage


def load_geotiff(layer_name):
    return geemap.load_GeoTIFF(f"gs://hotspotstoplight-sanjose-ui/{layer_name}_cog.tif")


@st.cache_data
def read_data(url):
    return gpd.read_file(url)


def create_map(layers, vizParams, site_urls, polygon_colors):
    Map = geemap.Map()
    Map.add_basemap("Esri.WorldImagery")

    # Add GeoTIFF layers
    for name, layer in layers.items():
        Map.addLayer(layer, vizParams[name], name)

    # Add GeoJSON layers
    for url in site_urls:
        name = url.split("/")[-1].split(".")[0]
        data = read_data(url)
        ee_layer = geemap.geopandas_to_ee(data)
        color = polygon_colors.get(name, "000000")
        Map.addLayer(
            ee_layer,
            {"color": color, "fillColor": "00000000", "fillOpacity": 0.0},
            name,
        )

    Map.add_basemap("CartoDB.PositronOnlyLabels")
    Map.centerObject(layers["bio"], 11)
    return Map


def display_site_visit_data(site_table_urls):
    st.write("## Site Visit Data")
    st.write(
        "The following table contains information about site visits to priority sites."
    )

    for url in site_table_urls:
        # Extract the table name from the URL
        table_name = url.split("/")[-1].split(".")[0]

        st.write(f"### {table_name}")
        st.write("")

        # Load the GeoJSON
        with st.spinner(f"Loading {url}..."):
            df = read_data(url)
            df = df.drop(
                columns=["geometry", "Shape_Area", "Shape_Length", "Label", "OBJECTID"]
            )

        # Display the table
        st.write(df)
        st.write("")
