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

@st.cache(persist=True)
def ee_authenticate(token_name="EARTHENGINE_TOKEN"):
    geemap.ee_initialize(token_name=token_name)

st.set_page_config(layout="wide")

st.title("Hotspot Stoplight Geospatial Data Viz")

st.markdown(
    """
    This app displays geospatial data for the Hotspot Stoplight trip to San Jose, Costa Rica in May of 2024. It is forked and modified from [Qiusheng Wu's work](https://github.com/giswqs/streamlit-multipage-template).
    """
)
