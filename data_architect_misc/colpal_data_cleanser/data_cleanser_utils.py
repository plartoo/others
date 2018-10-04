import pdb

import json

import account_info

# https://web.archive.org/web/20181002170353/https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b
def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

def print_config():
    pass



[
    # 'str','float', 'int', 'date'
    {
        'raw_column_name': '',
        'processed_column_name': 'Sector',
        'expected_data_type': 'str',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Subsector',
        'expected_data_type': 'str',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Advertiser',
        'expected_data_type': 'str',
        'null_allowed': False ####
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Category',
        'expected_data_type': 'str',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Brand',
        'expected_data_type': 'str',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Product',
        'expected_data_type': 'str',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Media',
        'expected_data_type': 'str',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Submedia1',
        'expected_data_type': 'str',
        'if_null': 'N/A' ####
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Submedia2',
        'expected_data_type': 'str',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Daypart',
        'expected_data_type': 'str',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Format',
        'expected_data_type': 'str',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Creative',
        'expected_data_type': 'str',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Network',
        'expected_data_type': 'str',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Channel',
        'expected_data_type': 'str',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Vehicle',
        'expected_data_type': 'str',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Total Duration',
        'expected_data_type': 'int',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Insertions',
        'expected_data_type': 'int',
    }
    , {
        'raw_column_name': 'Spot Length',
        'processed_column_name': '',
        'expected_data_type': 'int',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Impressions',
        'expected_data_type': 'int',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Geography',
        'expected_data_type': 'str',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Region',
        'expected_data_type': 'str',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Subregion',
        'expected_data_type': 'str',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'City',
        'expected_data_type': 'str',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Country',
        'expected_data_type': 'str',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Date',
        'expected_data_type': 'date',
        'pattern': r'' ####
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Currency',
        'expected_data_type': 'str',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Local Spend',
        'expected_data_type': 'float',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'Spend in USD',
        'expected_data_type': 'float',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'GRP',
        'expected_data_type': 'float',
    }
    , {
        'raw_column_name': '',
        'processed_column_name': 'GRP 30',
        'expected_data_type': 'float',
    }
    , { # [DM_1219_ColgateGlobal].[dbo].[CP_DIM_DEMOGRAPHIC]
        'raw_column_name': '',
        'processed_column_name': 'GRP Demographic',
        'expected_data_type': 'str',
    }
]
