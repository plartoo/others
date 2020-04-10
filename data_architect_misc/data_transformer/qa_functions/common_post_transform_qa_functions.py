"""
Include this python file in the common_post_transform_qa_config.json
file with the key like this:
"custom_transform_functions_file": "./transform_functions/common_post_transform_qa_functions.py",

and run the transform.py like this:
>> python transform.py

Author: Phyo Thiha
Last Modified: April 10, 2020
"""
import pandas as pd

from transform_functions.transform_functions import CommonTransformFunctions


class CustomFunctions:
    """
    This class is the collection of QA functions that must be run
    against the transformed data. The QA functions here will either
    give warnings or throw errors (if the impact is serious).
    """

    def test_qa(self, df) -> pd.DataFrame:
        """
        """
        import pdb
        pdb.set_trace()
        print('ah')
        return df
