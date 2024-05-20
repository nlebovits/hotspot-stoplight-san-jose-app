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
import janitor as jn
import pandas as pd

from utils.auth import (
    get_credentials,
    initialize_ee,
    get_storage_client,
    get_bucket_name,
)

# Initialize credentials and services
credentials = get_credentials()
initialize_ee(credentials)
storage_client = get_storage_client(credentials)
bucket_name = get_bucket_name()


def load_geotiff(layer_key, layers_dict):
    try:
        # Construct the filename based on the key and the provided dictionary
        layer_name = layers_dict[layer_key]
        file_path = f"gs://{bucket_name}/{layer_name}_cog.tif"
        # st.write(f"Loading GeoTIFF: {file_path}")  # Debugging statement
        return geemap.load_GeoTIFF(file_path)
    except Exception as e:
        st.error(f"Error loading GeoTIFF: {file_path}. Exception: {str(e)}")
        raise


@st.cache_data
def read_data(url):
    gdf = gpd.read_file(url)
    gdf = gdf.clean_names()
    return gdf


def create_map(layers, vizParams, site_table_urls, polygon_colors):
    Map = geemap.Map()
    Map.add_basemap("Esri.WorldImagery")

    # Add GeoTIFF layers
    for key, layer in layers.items():
        Map.addLayer(layer, vizParams[key], key)

    # Add GeoJSON layers
    for url in site_table_urls:
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
    combined_df = pd.DataFrame()

    for url in site_table_urls:
        # Load the GeoJSON
        with st.spinner(f"Loading {url}..."):
            df = read_data(url)
            df = df.drop(columns=["geometry", "shape_area", "shape_length", "objectid"])
            combined_df = pd.concat([combined_df, df], ignore_index=True)

    # Replace values in the 'label' column
    combined_df["label"] = combined_df["label"].replace(
        {
            "^B": "Bio ",
            "^C": "Climate ",
            "^X": "UrbEx",
            "^E": "Expansion ",
            "^U": "Urban ",
        },
        regex=True,
    )

    # Display the combined table
    st.write(combined_df)
    st.write("")
