import os
import zipfile

def unzip(source_folder, zip_file, dest_folder):
    zip_file_with_full_path = os.path.join(source_folder, zip_file)
    with zipfile.ZipFile(zip_file_with_full_path, 'r') as zip_file:
        zip_file.extractall(dest_folder)

def get_filesize(folder, file):
    """
    Return file size in bytes.
    """
    # return os.stat(file).st_size
    file_with_full_path = os.path.join(folder, file)
    return os.path.getsize(file_with_full_path)
