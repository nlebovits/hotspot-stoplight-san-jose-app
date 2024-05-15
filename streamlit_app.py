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
from google.oauth2 import service_account
import streamlit as st
import geopandas as gpd
import json
import base64

from utils.geoutils import load_geotiff

load_dotenv()

service_account_info = json.loads(base64.b64decode(st.secrets["GOOGLE_SERVICE_ACCOUNT_KEY"]))

credentials = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)
cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT_NAME")

ee.Initialize(credentials=credentials, project=cloud_project)

storage_client = storage.Client(credentials=credentials)

bucket = storage_client.bucket("hotspotstoplight-sanjose-ui")

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

# Palettes
palette_urban = ['FFFFE5', '004529']
palette_urbex = ['FFFFFF', 'E3B521']
palette_expansion = ['FFFFFF', '004DA8']
palette_climate = ['FFFFFF', '3F007D']
palette_bio = ['FFF7EC', '7F0000']

vizParams = {
    "bio": {'min': 0, 'max': 1, 'palette': palette_bio},
    "clim": {'min': 0, 'max': 1, 'palette': palette_climate},
    "urb": {'min': 0, 'max': 1, 'palette': palette_urban},
    "urbex": {'min': 0, 'max': 1, 'palette': palette_urbex},
    "expansion": {'min': 0, 'max': 1, 'palette': palette_expansion}
}

layers = {
    "bio": load_geotiff("bio"),
    "clim": load_geotiff("clim"),
    "urb": load_geotiff("urb"),
    "urbex": load_geotiff("urbex")# ,
    # "expansion": load_geotiff("expansion")
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

# Add GeoTIFF layers
for name, layer in layers.items():
    Map.addLayer(layer, vizParams[name], name)

# Add GeoJSON layers
for url in site_urls:
    name = url.split('/')[-1].split('.')[0]
    data = read_data(url)
    ee_layer = geemap.geopandas_to_ee(data)
    Map.addLayer(ee_layer, {'color': '000000', 'fillOpacity': 0.5}, name)

Map.add_basemap('CartoDB.PositronOnlyLabels')
Map.centerObject(layers['bio'], 11)

# Display the map
Map.to_streamlit(height=1000)
