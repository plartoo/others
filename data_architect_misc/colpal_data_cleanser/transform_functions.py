import pdb

import json

import account_info

# https://web.archive.org/web/20181002170353/https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b
def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

def print_config():
    pass

def remove_dollars(data_row):


    def multiply_by_thousand()