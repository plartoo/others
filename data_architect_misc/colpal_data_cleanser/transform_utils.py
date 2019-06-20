import json


USAGE = '''
Usage example:
>> python transform.py -c .\configs\china\config.json
'''

DESC = "This program transform raw data files according to the procedures and rules" \
       "set forth in the JSON configuration file, which is provided as input.\n " \
       "The output from this transform process is in CSV format " \
       "(with '|' as default delimiter)." + USAGE

HELP = "[Required] Configuration file (with full/relative path).\n" \
       "E.g., python transform.py -c .\configs\china\config.json"

CONFIG_FILE_ERROR = '''
ERROR: You must provide a valid path AND name of the JSON configuration file.
''' + USAGE

def load_config(config_file):
    # REF: https://web.archive.org/web/20181002170353/https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b
    with open(config_file, 'r') as f:
        return json.load(f)



# TODO: write generate_config_json function below

def print_config():
    pass
