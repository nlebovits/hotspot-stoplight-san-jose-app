import tempfile
import subprocess
import zipfile
import glob
import geemap
import ee
from google.cloud import storage
import os

def load_geotiff(layer_name):
    return geemap.load_GeoTIFF(f"gs://hotspotstoplight-sanjose-ui/{layer_name}_cog.tif")

def process_kmz_to_ee_feature(bucket, blob_name):
    blob = bucket.blob(blob_name)
    with tempfile.NamedTemporaryFile(suffix='.kmz', delete=False) as temp_file:
        blob.download_to_filename(temp_file.name)
        kmz_path = temp_file.name

    kml_path = kmz_path.replace('.kmz', '.kml')
    with zipfile.ZipFile(kmz_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(kml_path))
        kml_file = os.path.join(os.path.dirname(kml_path), 'doc.kml')

    shp_path = kmz_path.replace('.kmz', '.shp')
    cmd = f'ogr2ogr -f "ESRI Shapefile" {shp_path} {kml_file}'
    subprocess.run(cmd, shell=True, check=True)

    try:
        ee_object = geemap.shp_to_ee(shp_path)
    finally:
        # Cleanup: remove temporary files
        os.remove(kmz_path)
        os.remove(kml_file)
        for file in glob.glob(shp_path.replace('.shp', '.*')):
            os.remove(file)
    
    return ee_object