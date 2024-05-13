import os
import tempfile
import subprocess
import zipfile
import glob
import geemap
import ee
from google.cloud import storage
import logging
import shutil

def load_geotiff(layer_name):
    return geemap.load_GeoTIFF(f"gs://hotspotstoplight-sanjose-ui/{layer_name}_top_cluster_idx_cog.tif")


def process_kmz_to_ee_feature(bucket_name, blob_name):
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.get_bucket(bucket_name)

    # Determine the shapefile directory name on GCS and locally
    shapefile_dir_name = blob_name.replace('.kmz', '')
    local_shapefile_dir = os.path.join('data', shapefile_dir_name)

    # Ensure local data directory exists
    if not os.path.exists('data'):
        os.makedirs('data', exist_ok=True)

    # Check if the directory for the shapefile already exists in the bucket
    blobs = list(bucket.list_blobs(prefix=shapefile_dir_name))
    shapefile_exists_on_gcs = any(blob.name.endswith('.shp') for blob in blobs)

    # Check if the directory for the shapefile already exists locally
    local_files_exist = os.path.exists(os.path.join(local_shapefile_dir, shapefile_dir_name + '.shp'))

    if not local_files_exist:
        logging.info("Local shapefile directory does not exist, starting conversion and local saving.")
        # Convert KMZ to shapefile if it does not exist locally
        with tempfile.TemporaryDirectory() as temp_dir:
            kmz_path = os.path.join(temp_dir, 'temp.kmz')
            kml_path = os.path.join(temp_dir, 'doc.kml')

            # Download KMZ file from Google Cloud Storage
            blob = bucket.blob(blob_name)
            try:
                blob.download_to_filename(kmz_path)
                logging.info("KMZ file downloaded successfully.")
            except Exception as e:
                logging.error(f"Failed to download KMZ file: {e}")
                return None

            # Extract KMZ to get the KML file
            try:
                with zipfile.ZipFile(kmz_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                logging.info("KMZ file extracted successfully.")
            except Exception as e:
                logging.error(f"Failed to extract KMZ file: {e}")
                return None

            # Convert KML to a Shapefile directory
            shp_path = os.path.join(temp_dir, shapefile_dir_name)
            os.makedirs(shp_path, exist_ok=True)
            cmd = f'ogr2ogr -f "ESRI Shapefile" {shp_path} {kml_path}'
            try:
                subprocess.run(cmd, shell=True, check=True)
                logging.info("Shapefile conversion successful.")
            except Exception as e:
                logging.error(f"Shapefile conversion failed: {e}")
                return None

            # Save locally
            if not os.path.exists(local_shapefile_dir):
                os.makedirs(local_shapefile_dir)
            copy_shapefile_folder(shp_path, local_shapefile_dir)

    # Upload to GCS if not already present
    if not shapefile_exists_on_gcs:
        logging.info("Shapefile not found on GCS, uploading.")
        upload_shapefile_folder(bucket, shapefile_dir_name, os.path.join('data', shapefile_dir_name))

    # Assuming shapefile directory is now present locally, load into Earth Engine
    try:
        ee_object = geemap.shp_to_ee(f"gs://{bucket_name}/{shapefile_dir_name}")
        logging.info("Shapefile loaded into Earth Engine successfully.")
        return ee_object
    except Exception as e:
        logging.error(f"Failed to load shapefile into Earth Engine: {e}")
        return None

def upload_shapefile_folder(bucket, blob_name, folder_path):
    # Upload all files within the shapefile directory to the bucket
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, start=folder_path)
            blob = bucket.blob(os.path.join(blob_name, rel_path))
            blob.upload_from_filename(file_path)
            logging.info(f"Uploaded {rel_path} to GCS.")

def copy_shapefile_folder(source_path, destination_path):
    # Copy all files within the shapefile directory to the local folder
    for root, dirs, files in os.walk(source_path):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, start=source_path)
            local_file_path = os.path.join(destination_path, rel_path)
            shutil.copy(file_path, local_file_path)
            logging.info(f"Copied {rel_path} to local directory.")