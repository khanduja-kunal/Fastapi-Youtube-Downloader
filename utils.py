import os

# Utility function to create the 'downloads' directory if it doesn't exist
def create_download_directory(download_dir: str):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
