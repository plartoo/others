"""
Sample data transformation script
that can be invoked via
convert_to_txt_and_transform.py script.
"""

import pandas as pd

def transform_data(dataframe):
    dataframe['TestForTransformData'] = 'whatupdoc'
    return dataframe
