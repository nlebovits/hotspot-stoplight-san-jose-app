import streamlit as st

from utils.auth import (
    get_bucket_name,
    get_credentials,
    get_storage_client,
    initialize_ee,
)
from utils.config import (
    LAYERS_CLUSTERING,
    POLYGON_COLORS,
    SITE_URLS,
    VIZ_PARAMS_CLUSTERING,
    set_page_config,
    set_title,
    sidebar_setup,
)
from utils.geoutils import create_map, load_geotiff

# Authentication and Initialization
credentials = get_credentials()
initialize_ee(credentials)
storage_client = get_storage_client(credentials)
bucket_name = get_bucket_name()
bucket = storage_client.bucket(bucket_name)

# Streamlit Configuration
set_page_config()
sidebar_setup()
set_title()

# Load GeoTIFF layers
layers = {name: load_geotiff(layer) for name, layer in LAYERS_CLUSTERING.items()}

# Create and display the map
Map = create_map(layers, VIZ_PARAMS_CLUSTERING, SITE_URLS, POLYGON_COLORS)
Map.to_streamlit(height=1000)
