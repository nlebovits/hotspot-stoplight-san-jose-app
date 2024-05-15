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
