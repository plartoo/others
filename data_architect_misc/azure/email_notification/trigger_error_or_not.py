"""
Last Modified: May 16, 2019
Author: Phyo Thiha
Description:
Script that throws error (or not) based on 'throw_error' flag.
This is used to test whether we can leverage conditional branching
in Azure Data Factory.
"""

import json


class MadeUpError(Exception):
    """Custom error to test conditional branching in Azure Data Factory"""
    pass


def main():
    """
    # JSON below is only for testing on your laptop; on production environment, we'll use step 2a. instead
    json_activity = {
        'typeProperties':
            {
                'extendedProperties':
                    {
                        'throw_error': '1',
                    }
            }
    }
    """

    # 1. get 'Extended Properties' passed from Azure Data Factory task
    read_activity = open('activity.json').read()
    json_activity = json.loads(read_activity)
    #"""

    throw_error = int(json_activity['typeProperties']['extendedProperties']['throw_error'])
    if throw_error:
        print("Error")
        raise MadeUpError
    else:
        print("Success")


if __name__ == '__main__':
    main()