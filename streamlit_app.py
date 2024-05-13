import os
from dotenv import load_dotenv
import ee
import geemap
import colorcet
import requests
import json
from google.cloud import storage
import tempfile
import streamlit as st
import subprocess
import zipfile
import glob

load_dotenv()

cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT_NAME")
key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ["GDAL_DISABLE_READDIR_ON_OPEN"] = "YES"
os.environ["CPL_VSIL_CURL_ALLOWED_EXTENSIONS"] = "tif"


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


storage_client = storage.Client()
bucket = storage_client.bucket("hotspotstoplight-sanjose-ui")

ee.Authenticate()
ee.Initialize(project=cloud_project)

bio = geemap.load_GeoTIFF("gs://hotspotstoplight-sanjose-ui/bio_top_cluster_idx_cog.tif")
clim = geemap.load_GeoTIFF("gs://hotspotstoplight-sanjose-ui/clim_top_cluster_idx_cog.tif")
urb = geemap.load_GeoTIFF("gs://hotspotstoplight-sanjose-ui/urb_top_cluster_idx_cog.tif")
urbex = geemap.load_GeoTIFF("gs://hotspotstoplight-sanjose-ui/urbex_top_cluster_idx_cog.tif")

def process_kmz_to_ee_feature(bucket, blob_name):
    blob = bucket.blob(blob_name)
    
    # Download the KMZ file to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.kmz', delete=False) as temp_file:
        blob.download_to_filename(temp_file.name)
        kmz_path = temp_file.name

    # Unzip KMZ to extract the KML file
    kml_path = kmz_path.replace('.kmz', '.kml')
    with zipfile.ZipFile(kmz_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(kml_path))
        kml_file = os.path.join(os.path.dirname(kml_path), 'doc.kml')

    # Convert KML to SHP using GDAL's ogr2ogr
    shp_path = kmz_path.replace('.kmz', '.shp')
    cmd = f'ogr2ogr -f "ESRI Shapefile" {shp_path} {kml_file}'
    subprocess.run(cmd, shell=True, check=True)

    # Convert SHP to Earth Engine object
    ee_object = None
    try:
        ee_object = geemap.shp_to_ee(shp_path)
        print(f"Conversion to Earth Engine object successful for {blob_name}.")
    except Exception as e:
        print(f"Failed to convert SHP to Earth Engine object for {blob_name}:", e)

    # Cleanup: remove temporary files
    os.remove(kmz_path)
    os.remove(kml_file)
    for file in glob.glob(shp_path.replace('.shp', '.*')):
        os.remove(file)
    
    return ee_object

# Initialize your map
Map = geemap.Map()

# List of blob names
blob_names = [
    'Priority_Zones_Clim_SiteVisit.kmz',
    'Priority_Zones_Bio_SiteVisit.kmz',
    'Priority_Zones_Urb_SiteVisit.kmz',
    'Priority_Zones_UrbEx_SiteVisit.kmz',
    'Priority_Zones_Expansion_SiteVisit.kmz'
]





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
# Process each KMZ and add as a layer to the map
for blob_name in blob_names:
    ee_feature = process_kmz_to_ee_feature(bucket, blob_name)
    if ee_feature is not None:
        Map.addLayer(ee_feature, {}, blob_name.split('.')[0])
# Map.addLayer(bio_zones, {}, "bio zones")
# Map.addLayer(image, vizParamsProbability, "Flood Prob")
Map.add_basemap('CartoDB.PositronOnlyLabels')
Map.centerObject(bio, 11)

with col1:

    Map.to_streamlit(height=1000)