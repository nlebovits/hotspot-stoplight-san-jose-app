import base64
import json
import os

import ee
from dotenv import load_dotenv
from google.cloud import storage
from google.oauth2 import service_account

load_dotenv()


def get_credentials():
    service_account_info = json.loads(
        base64.b64decode(os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY"))
    )
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    return credentials


def initialize_ee(credentials):
    cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT_NAME")
    ee.Initialize(credentials=credentials, project=cloud_project)


def get_storage_client(credentials):
    return storage.Client(credentials=credentials)
