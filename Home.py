import leafmap.foliumap as leafmap
import streamlit as st

st.set_page_config(layout="wide")

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
