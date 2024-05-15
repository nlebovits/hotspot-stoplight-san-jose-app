import streamlit as st

from utils.auth import get_credentials, get_storage_client, initialize_ee
from utils.config import set_page_config, set_title, sidebar_setup
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

# Palettes
palette_urban = ["FFFFE5", "004529"]
palette_urbex = ["FFFFFF", "E3B521"]
palette_expansion = ["FFFFFF", "004DA8"]
palette_climate = ["FFFFFF", "3F007D"]
palette_bio = ["FFF7EC", "7F0000"]

vizParams = {
    "bio": {"min": 0, "max": 1, "palette": palette_bio},
    "clim": {"min": 0, "max": 1, "palette": palette_climate},
    "urb": {"min": 0, "max": 1, "palette": palette_urban},
    "urbex": {"min": 0, "max": 1, "palette": palette_urbex},
    "expansion": {"min": 0, "max": 1, "palette": palette_expansion},
}

layers = {
    "bio": load_geotiff("bio_top_cluster_idx"),
    "clim": load_geotiff("clim_top_cluster_idx"),
    "urb": load_geotiff("urb_top_cluster_idx"),
    "urbex": load_geotiff("urbex_top_cluster_idx")  # ,
    # "expansion": load_geotiff("expansion")
}

site_urls = [
    "https://github.com/HotspotStoplight/HotspotStoplight/raw/main/WebMap/geojson/Priority_Bio_SiteVisit.geojson",
    "https://github.com/HotspotStoplight/HotspotStoplight/raw/main/WebMap/geojson/Priority_Clim_SiteVisit.geojson",
    "https://github.com/HotspotStoplight/HotspotStoplight/raw/main/WebMap/geojson/Priority_Urb_SiteVisit.geojson",
    "https://github.com/HotspotStoplight/HotspotStoplight/raw/main/WebMap/geojson/Priority_UrbEx_SiteVisit.geojson",
    "https://github.com/HotspotStoplight/HotspotStoplight/raw/main/WebMap/geojson/Priority_Expansion_SiteVisit.geojson",
]

polygon_colors = {
    "Priority_Bio_SiteVisit": "E60000",
    "Priority_Clim_SiteVisit": "A900E6",
    "Priority_Urb_SiteVisit": "4CE600",
    "Priority_UrbEx_SiteVisit": "E6E600",
    "Priority_Expansion_SiteVisit": "0070FF",
}

# Create and display the map
Map = create_map(layers, vizParams, site_urls, polygon_colors)
Map.to_streamlit(height=1000)
