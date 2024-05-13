import os
from dotenv import load_dotenv
import ee
import geemap
import colorcet
from google.cloud import storage
from google.oauth2 import service_account
import tempfile
import subprocess
import zipfile
import glob
import streamlit as st
import base64
from utils.geoutils import load_geotiff, process_kmz_to_ee_feature
import json

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


Map = geemap.Map()
Map.add_basemap('Esri.WorldImagery')
for name, layer in layers.items():
    Map.addLayer(layer, vizParams[name], name)

blob_names = [
    'Priority_Zones_Clim_SiteVisit.kmz',
    'Priority_Zones_Bio_SiteVisit.kmz',
    'Priority_Zones_Urb_SiteVisit.kmz',
    'Priority_Zones_UrbEx_SiteVisit.kmz',
    'Priority_Zones_Expansion_SiteVisit.kmz'
]
for blob_name in blob_names:
    ee_feature = process_kmz_to_ee_feature(bucket, blob_name)
    if ee_feature:
        Map.addLayer(ee_feature, {}, blob_name.split('.')[0])

Map.add_basemap('CartoDB.PositronOnlyLabels')
Map.centerObject(layers['bio'], 11)

# Display the map
Map.to_streamlit(height=1000)
