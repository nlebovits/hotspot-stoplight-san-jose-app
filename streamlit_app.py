import streamlit as st

from utils.config import (
    LAYERS_CLUSTERING,
    LAYERS_CONTRIBUTING,
    POLYGON_COLORS,
    SITE_TABLE_URLS,
    VIZ_PARAMS_CLUSTERING,
    VIZ_PARAMS_CONTRIBUTING,
    set_page_config,
    set_title,
    sidebar_setup,
)

from utils.geoutils import create_map, display_site_visit_data, load_geotiff
from utils.auth import (
    get_credentials,
    initialize_ee,
    get_storage_client,
    get_bucket_name,
)

# Initialize credentials and services
credentials = get_credentials()
initialize_ee(credentials)
storage_client = get_storage_client(credentials)
bucket_name = get_bucket_name()

set_page_config()

sidebar_setup()

# set_title()

# Define a page selection for different maps
page = st.sidebar.selectbox("Choose a map type", ["Clustering", "Contributing"])

st.sidebar.markdown(
    """
    <div style='text-align: center;'>
        This web app displays data related to the Hotspot Stoplight Costa Rica groundtruthing mission in May 2024.
    </div>
""",
    unsafe_allow_html=True,
)

# Load and visualize layers based on the selected page
if page == "Clustering":
    layers_dict = LAYERS_CLUSTERING
    viz_params = VIZ_PARAMS_CLUSTERING
elif page == "Contributing":
    layers_dict = LAYERS_CONTRIBUTING
    viz_params = VIZ_PARAMS_CONTRIBUTING

# Load the layers
layers = {key: load_geotiff(key, layers_dict) for key in layers_dict}

# Create and display the map
map = create_map(layers, viz_params, SITE_TABLE_URLS, POLYGON_COLORS)
map.to_streamlit(height=700)

# Display site visit data
display_site_visit_data(SITE_TABLE_URLS)
