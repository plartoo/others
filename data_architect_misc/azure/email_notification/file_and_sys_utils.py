import os
import sys


def get_full_path(dir_name):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), dir_name)


def remove_contents_in_folder(dir_path):
    # Removes all files and folders that reside in a given folder
    for c in os.listdir(dir_path):
        full_path = os.path.join(dir_path, c)
        if os.path.isfile(full_path):
            os.remove(full_path)
        else:
            shutil.rmtree(full_path)


def list_files_ending_with(dir_path, file_extension):
    files = []
    for file in os.listdir(dir_path):
        if file.endswith(file_extension):
            files.append(os.path.join(dir_path,file))
    return files


def append_new_sys_path(dir_name):
    new_sys_path = get_full_path(dir_name)
    if new_sys_path not in sys.path:
        sys.path.append(new_sys_path)
        print("\nNew sys path appended:", new_sys_path)
        print("Current sys path is:\n", sys.path, "\n")


def create_unique_local_download_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def join_path_and_file_name(path, file_name, separator=os.sep):
    # Note: I can combine the following lines into one line of code,
    # but I won't because of better readability
    normalized_path = os.path.normpath(path)
    file_name_with_path = os.path.join(normalized_path, file_name).split(os.sep)
    return separator.join(file_name_with_path)
