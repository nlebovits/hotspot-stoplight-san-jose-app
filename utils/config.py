import streamlit as st


def set_page_config():
    st.set_page_config(layout="wide")


def sidebar_setup():
    # st.sidebar.markdown("<h1 style='text-align: center;'>Hotspot Stoplight Web App</h1>", unsafe_allow_html=True)
    logo = "https://github.com/nlebovits/hotspot-stoplight-san-jose-app/raw/master/assets/logo.png"
    st.sidebar.image(logo)

    # Centered content using HTML
    html_content = """
    <div style="text-align: center;">
        <p><a href="https://hotspot-stoplight-san-jose.streamlit.app/">Web App URL</a></p>
        <p><a href="https://github.com/nlebovits/hotspot-stoplight-san-jose-app">GitHub Repository</a></p>
    </div>
    """
    st.sidebar.markdown(html_content, unsafe_allow_html=True)


def set_title():
    st.title("Hotspot Stoplight Geospatial Data Viz")
    st.markdown(
        """
        This app displays geospatial data for the Hotspot Stoplight trip to San Jose, Costa Rica in May of 2024. It is forked and modified from [Qiusheng Wu's work](https://github.com/giswqs/streamlit-multipage-template).
        """
    )


# URLs for GeoJSON files
SITE_URLS = [
    "https://github.com/HotspotStoplight/HotspotStoplight/raw/main/WebMap/geojson/Priority_Bio_SiteVisit.geojson",
    "https://github.com/HotspotStoplight/HotspotStoplight/raw/main/WebMap/geojson/Priority_Clim_SiteVisit.geojson",
    "https://github.com/HotspotStoplight/HotspotStoplight/raw/main/WebMap/geojson/Priority_Urb_SiteVisit.geojson",
    "https://github.com/HotspotStoplight/HotspotStoplight/raw/main/WebMap/geojson/Priority_UrbEx_SiteVisit.geojson",
    "https://github.com/HotspotStoplight/HotspotStoplight/raw/main/WebMap/geojson/Priority_Expansion_SiteVisit.geojson",
]

# Polygon colors for GeoJSON files
POLYGON_COLORS = {
    "Priority_Bio_SiteVisit": "E60000",
    "Priority_Clim_SiteVisit": "A900E6",
    "Priority_Urb_SiteVisit": "4CE600",
    "Priority_UrbEx_SiteVisit": "E6E600",
    "Priority_Expansion_SiteVisit": "0070FF",
}

# Palettes for visualization parameters
PALETTE_URBAN = ["FFFFE5", "004529"]
PALETTE_URBEX = ["FFFFFF", "E3B521"]
PALETTE_EXPANSION = ["FFFFFF", "004DA8"]
PALETTE_CLIMATE = ["FFFFFF", "3F007D"]
PALETTE_BIO = ["FFF7EC", "7F0000"]
PALETTE_BII = ["FFF7EC", "7F0000"]
PALETTE_FLOOD = ["FFFFFF", "0033CC"]
PALETTE_HEAT = ["FFFFFF", "FF0000"]
PALETTE_LCC = ["FFFFFF", "00FF00"]
PALETTE_POP = ["FFFFFF", "800080"]

# Visualization parameters
VIZ_PARAMS_CLUSTERING = {
    "bio": {"min": 0, "max": 1, "palette": PALETTE_BIO},
    "clim": {"min": 0, "max": 1, "palette": PALETTE_CLIMATE},
    "urb": {"min": 0, "max": 1, "palette": PALETTE_URBAN},
    "urbex": {"min": 0, "max": 1, "palette": PALETTE_URBEX},
    "expansion": {"min": 0, "max": 1, "palette": PALETTE_EXPANSION},
}

VIZ_PARAMS_CONTRIBUTING = {
    "bii": {"min": 0, "max": 1, "palette": PALETTE_BII},
    "anthro": {"min": 0, "max": 1, "palette": PALETTE_CLIMATE},
    "urban": {"min": 0, "max": 1, "palette": PALETTE_URBAN},
    "flood": {"min": 0, "max": 1, "palette": PALETTE_FLOOD},
    "heat": {"min": 0, "max": 1, "palette": PALETTE_HEAT},
    "lcc": {"min": 0, "max": 1, "palette": PALETTE_LCC},
    "pop": {"min": 0, "max": 1, "palette": PALETTE_POP},
    "bio": {"min": 0, "max": 1, "palette": PALETTE_BIO},
}

# Layer names for loading GeoTIFFs
LAYERS_CLUSTERING = {
    "bio": "bio_top_cluster_idx",
    "clim": "clim_top_cluster_idx",
    "urb": "urb_top_cluster_idx",
    "urbex": "urbex_top_cluster_idx",
    "expansion": "urb_cluster0_idx",
}

LAYERS_CONTRIBUTING = {
    "bii": "bii",
    "anthro": "anthro_risk_norm",
    "bio": "bio_risk_norm",
    "flood": "flood_hazards",
    "heat": "heat_hazards",
    "lcc": "lcc_probability",
    "pop": "population",
    "urban": "urban_probability",
}

SITE_TABLE_URLS = [
    "https://github.com/HotspotStoplight/HotspotStoplight/raw/main/WebMap/geojson/geojsons_extracted_distributions/Priority_Bio_SiteVisit.geojson",
    "https://github.com/HotspotStoplight/HotspotStoplight/raw/main/WebMap/geojson/geojsons_extracted_distributions/Priority_Clim_SiteVisit.geojson",
    "https://github.com/HotspotStoplight/HotspotStoplight/raw/main/WebMap/geojson/geojsons_extracted_distributions/Priority_Expansion_SiteVisit.geojson",
    "https://github.com/HotspotStoplight/HotspotStoplight/raw/main/WebMap/geojson/geojsons_extracted_distributions/Priority_UrbEx_SiteVisit.geojson",
    "https://github.com/HotspotStoplight/HotspotStoplight/raw/main/WebMap/geojson/geojsons_extracted_distributions/Priority_Urb_SiteVisit.geojson",
]
