import os
from dotenv import load_dotenv
import ee
import geemap
from geemap import geojson_to_ee
import colorcet
from google.cloud import storage
import tempfile
import subprocess
import zipfile
import glob
import streamlit as st
import geopandas as gpd

from utils.geoutils import load_geotiff

load_dotenv()

cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT_NAME")
storage_client = storage.Client()
bucket = storage_client.bucket("hotspotstoplight-sanjose-ui")
ee.Initialize(project=cloud_project)

st.set_page_config(layout="wide")
st.sidebar.title("About")
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)
markdown = """
Web App URL: <https://hotspot-stoplight-san-jose.streamlit.app/>
GitHub Repository: <https://github.com/nlebovits/hotspot-stoplight-san-jose-app>
"""
st.sidebar.info(markdown)
st.title("Hotspot Stoplight Geospatial Data Viz")
st.markdown("""
    This app displays geospatial data for the Hotspot Stoplight trip to San Jose, Costa Rica in May of 2024. It is forked and modified from [Qiusheng Wu's work](https://github.com/giswqs/streamlit-multipage-template).
""")

vizParams = {
    "bio": {'min': 0, 'max': 1, 'palette': colorcet.rainbow},
    "clim": {'min': 0, 'max': 1, 'palette': colorcet.fire},
    "urb": {'min': 0, 'max': 1, 'palette': colorcet.bmy},
    "urbex": {'min': 0, 'max': 1, 'palette': colorcet.bmw}
}

layers = {
    "bio": load_geotiff("bio"),
    "clim": load_geotiff("clim"),
    "urb": load_geotiff("urb"),
    "urbex": load_geotiff("urbex")
}

@st.cache_data
def read_data(url):
    return gpd.read_file(url)

site_urls = [
    'https://github.com/HotspotStoplight/HotspotStoplight/raw/main/WebMap/geojson/Priority_Bio_SiteVisit.geojson',
    'https://github.com/HotspotStoplight/HotspotStoplight/raw/main/WebMap/geojson/Priority_Clim_SiteVisit.geojson',
    'https://github.com/HotspotStoplight/HotspotStoplight/raw/main/WebMap/geojson/Priority_Urb_SiteVisit.geojson',
    'https://github.com/HotspotStoplight/HotspotStoplight/raw/main/WebMap/geojson/Priority_UrbEx_SiteVisit.geojson',
    'https://github.com/HotspotStoplight/HotspotStoplight/raw/main/WebMap/geojson/Priority_Expansion_SiteVisit.geojson'
]

Map = geemap.Map()
Map.add_basemap('Esri.WorldImagery')

# Add GeoJSON layers
for url in site_urls:
    name = url.split('/')[-1].split('.')[0]
    data = read_data(url)
    ee_layer = geemap.geopandas_to_ee(data)
    Map.addLayer(ee_layer, {}, name)

# Add GeoTIFF layers
for name, layer in layers.items():
    Map.addLayer(layer, vizParams[name], name)

Map.add_basemap('CartoDB.PositronOnlyLabels')
Map.centerObject(layers['bio'], 11)

# Display the map
Map.to_streamlit(height=1000)
