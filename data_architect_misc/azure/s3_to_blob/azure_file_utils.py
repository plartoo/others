import os


def create_unique_local_download_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def join_path_and_file_name(path, file_name, separator=os.sep):
    # Note: I can combine the following lines into one line of code,
    # but I won't because of better readability
    normalized_path = os.path.normpath(path)
    file_name_with_path = os.path.join(normalized_path, file_name).split(os.sep)
    return separator.join(file_name_with_path)
