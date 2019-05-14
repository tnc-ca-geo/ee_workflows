"""
Copy assets from a local data folder to EE via Google Cloud
"""
import argparse
import importlib
import subprocess
import os
import ee
from google.cloud import storage


GS_BUCKET = 'gde_data'


# from https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """
    Uploads a file to the bucket.
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


def move_to_ee(src, dest, user):
    print('\nMove to ee\n')
    cmd = [
        'earthengine', 'upload', 'table',
        '--asset_id=users/{}/{}'.format(user, dest),
        'gs://{}/{}'.format(GS_BUCKET, src)]
    print(cmd)
    p = subprocess.run(cmd, stdout=subprocess.PIPE)
    print(p.stdout)


def main(ee_path, directory):
    cmd = ['earthengine', 'create', 'folder', ee_path]
    subprocess.run(cmd, stdout=subprocess.PIPE)
    ee_path = ee_path.replace('users/', '')
    files = [os.path.join(directory, item) for item in os.listdir(directory)]
    for item in files:
        gs_dest_name = os.path.basename(item)
        gs_dest = 'ee_workflows/{}'.format(gs_dest_name)
        print('Copying {} to {}'.format(item, gs_dest))
        upload_blob(GS_BUCKET, item, gs_dest)
        move_to_ee(gs_dest, gs_dest_name.replace('.zip', ''), ee_path)
    print(
        '\n\nPlease check the Earthengine in about 10 minutes whether tasks'
        'have finished and assets successfully created.')


if __name__ == '__main__':
    default_file_location = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '..', '..', 'ee_data', 'example'))
    parser = argparse.ArgumentParser(
        description='Upload Earthengine assets')
    parser.add_argument(
        '-a', '--assetfolder', help='Asset folder', type=str,
        default='users/carogistnc/example')
    parser.add_argument(
        '-d', '--localdirectory', help='Local directory', type=str,
        default=default_file_location)
    args = parser.parse_args()
    main(args.assetfolder, args.localdirectory)
