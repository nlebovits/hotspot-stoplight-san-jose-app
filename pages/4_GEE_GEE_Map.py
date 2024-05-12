import ee
import geemap
import colorcet
import streamlit as st

st.set_page_config(layout="wide")


@st.cache(persist=True)
def ee_authenticate(token_name="EARTHENGINE_TOKEN"):
    geemap.ee_initialize(token_name=token_name)


st.sidebar.info(
    """
    - Web App URL: <https://streamlit.geemap.org>
    - GitHub repository: <https://github.com/giswqs/streamlit-geospatial>
    """
)


st.title("Google Earth Engine Map")

col1, col2 = st.columns([8, 2])

ee.Initialize(project='hotspotstoplight')

URL = 'gs://hotspotstoplight_floodmapping/data/united_kingdom_of_great_britain_and_northern_ireland/outputs/flood_prob0000000000-0000000000.tif'
image = geemap.load_GeoTIFF(URL)

Map = geemap.Map()
# Visualization parameters for probability with white at the midpoint
vizParamsProbability = {
    'min': 0,
    'max': 1,
    'palette': colorcet.rainbow #bmw # ['white', 'pink']#
}

Map.add_basemap('Esri.WorldImagery')
Map.addLayer(image, vizParamsProbability, "Prediction")
Map.add_basemap('CartoDB.PositronOnlyLabels')
Map.centerObject(image.geometry(), 8)
Map

with col1:

    Map.to_streamlit(height=1000)