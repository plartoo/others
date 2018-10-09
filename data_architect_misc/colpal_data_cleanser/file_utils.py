import pathlib

def get_file_extension(file_name):
    return pathlib.Path(file_name).suffix
