import base64
import json
import os

import ee
from google.cloud import storage
from google.oauth2 import service_account
import streamlit as st


def get_credentials():
    service_account_info = json.loads(
        base64.b64decode(st.secrets["GOOGLE_SERVICE_ACCOUNT_KEY"])
    )
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    return credentials


def initialize_ee(credentials):
    cloud_project = st.secrets["GOOGLE_CLOUD_PROJECT_NAME"]
    ee.Initialize(credentials=credentials, project=cloud_project)


def get_storage_client(credentials):
    return storage.Client(credentials=credentials)


def get_bucket_name():
    return st.secrets["GOOGLE_CLOUD_BUCKET_NAME"]
