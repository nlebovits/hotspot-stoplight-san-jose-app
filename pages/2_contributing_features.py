import streamlit as st

from utils.auth import get_credentials, get_storage_client, initialize_ee
from utils.config import (
    LAYERS_CONTRIBUTING,
    POLYGON_COLORS,
    SITE_URLS,
    VIZ_PARAMS_CONTRIBUTING,
    set_page_config,
    set_title,
    sidebar_setup,
)
from utils.geoutils import create_map, load_geotiff

# Authentication and Initialization
credentials = get_credentials()
initialize_ee(credentials)
storage_client = get_storage_client(credentials)
bucket = storage_client.bucket("hotspotstoplight-sanjose-ui")

# Streamlit Configuration
set_page_config()
sidebar_setup()
set_title()

# Load GeoTIFF layers
layers = {name: load_geotiff(layer) for name, layer in LAYERS_CONTRIBUTING.items()}

# Create and display the map
Map = create_map(layers, VIZ_PARAMS_CONTRIBUTING, SITE_URLS, POLYGON_COLORS)
Map.to_streamlit(height=1000)
