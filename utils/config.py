import streamlit as st


def set_page_config():
    st.set_page_config(layout="wide")


def sidebar_setup():
    st.sidebar.title("About")
    logo = "https://github.com/nlebovits/hotspot-stoplight-san-jose-app/raw/master/assets/logo.png"
    st.sidebar.image(logo)
    markdown = """
    [Web App URL](https://hotspot-stoplight-san-jose.streamlit.app/) |
    [GitHub Repository](https://github.com/nlebovits/hotspot-stoplight-san-jose-app)
    """
    st.sidebar.info(markdown)


def set_title():
    st.title("Hotspot Stoplight Geospatial Data Viz")
    st.markdown(
        """
        This app displays geospatial data for the Hotspot Stoplight trip to San Jose, Costa Rica in May of 2024. It is forked and modified from [Qiusheng Wu's work](https://github.com/giswqs/streamlit-multipage-template).
        """
    )
