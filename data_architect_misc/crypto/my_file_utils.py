import pdb

import os
import shutil

class MyFileUtils(object):

    @classmethod
    def create_folder(cls, folder_name, path=None):
        dir_path = os.path.dirname(os.path.realpath(__file__)) if not path else path
        output_dir = os.path.join(dir_path, folder_name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)


    @classmethod
    def remove_folder(cls, dir_path, folder_name, remove_everything=False):
        dir_to_delete = os.path.join(dir_path, folder_name)
        if remove_everything:
            shutil.rmtree(dir_to_delete)
        else:
            os.removedirs(dir_to_delete)


