import streamlit as st

from utils.config import (
    LAYERS_CLUSTERING,
    POLYGON_COLORS,
    SITE_TABLE_URLS,
    SITE_URLS,
    VIZ_PARAMS_CLUSTERING,
    set_page_config,
    set_title,
    sidebar_setup,
)

set_page_config()

sidebar_setup()

set_title()
