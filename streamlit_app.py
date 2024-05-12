import os
from dotenv import load_dotenv

import ee
import geemap
import colorcet
import requests
from google.cloud import storage
import streamlit as st

load_dotenv()

cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT_NAME")
key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ["GDAL_DISABLE_READDIR_ON_OPEN"] = "YES"
os.environ["CPL_VSIL_CURL_ALLOWED_EXTENSIONS"] = "tif"


print(key_path)

st.set_page_config(layout="wide")


@st.cache(persist=True)
def ee_authenticate(token_name="EARTHENGINE_TOKEN"):
    geemap.ee_initialize(token_name=token_name)

# Customize the sidebar
markdown = """
Web App URL: <https://hotspot-stoplight-san-jose.streamlit.app/>
GitHub Repository: <https://github.com/nlebovits/hotspot-stoplight-san-jose-app>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Customize page title
st.title("Hotspot Stoplight Geospatial Data Viz")

st.markdown(
    """
    This app displays geospatial data for the Hotspot Stoplight trip to San Jose, Costa Rica in May of 2024. It is forked and modified from [Qiusheng Wu's work](https://github.com/giswqs/streamlit-multipage-template).
    """
)

col1, col2 = st.columns([8, 2])

## connect to GCS
storage_client = storage.Client()
bucket = storage_client.bucket("hotspotstoplight-sanjose-ui")

ee.Authenticate()
ee.Initialize(project=cloud_project)

bio = geemap.load_GeoTIFF("gs://hotspotstoplight-sanjose-ui/bio_top_cluster_idx_cog.tif")
clim = geemap.load_GeoTIFF("gs://hotspotstoplight-sanjose-ui/clim_top_cluster_idx_cog.tif")
urb = geemap.load_GeoTIFF("gs://hotspotstoplight-sanjose-ui/urb_top_cluster_idx_cog.tif")
urbex = geemap.load_GeoTIFF("gs://hotspotstoplight-sanjose-ui/urbex_top_cluster_idx_cog.tif")


Map = geemap.Map()

vizParamsBio = {
    'min': 0,
    'max': 1,
    'palette': colorcet.rainbow #bmw # ['white', 'pink']#
}

vizParamsClim = {
    'min': 0,
    'max': 1,
    'palette': colorcet.fire
}

vizParamsUrb= {
    'min': 0,
    'max': 1,
    'palette': colorcet.bmy
}

vizParamsUrbex = {
    'min': 0,
    'max': 1,
    'palette': colorcet.bmw
}

Map.add_basemap('Esri.WorldImagery')
Map.addLayer(bio, vizParamsBio, "bio")
Map.addLayer(clim, vizParamsClim, "clim")
Map.addLayer(urb, vizParamsUrb, "urban")
Map.addLayer(urbex, vizParamsUrbex, "urbex")
# Map.addLayer(image, vizParamsProbability, "Flood Prob")
Map.add_basemap('CartoDB.PositronOnlyLabels')
Map.centerObject(bio, 11)

with col1:

    Map.to_streamlit(height=1000)