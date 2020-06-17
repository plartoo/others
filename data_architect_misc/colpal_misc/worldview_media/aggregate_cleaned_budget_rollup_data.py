import pdb

import argparse
import os

import pandas as pd

DELIMITER = '|'

DESC = """
Script to aggregate budget roll-up data in slightly 
different way to support different views in WorldView Media 
dashboard.
"""
I_FLAG_HELP_TEXT = """Use '-i' flag to enter the full path 
and the file name of the (cleaned/transformed) budget roll-up 
data that you want to aggregate. 
"""


class BudgetDataAggregationError(Exception):
    """Base class for budget roll-up data aggregation related exceptions."""
    def __str__(self):
        return f"\nERROR: {''.join(self.args)}"


class BudgetFileNotFoundError(BudgetDataAggregationError):
    def __init__(self, error_msg):
        super().__init__(error_msg)


def create_aggregate_data_for_market_investment_trend(df):
    pass


def main():
    parser = argparse.ArgumentParser(
        description=DESC,
        formatter_class=argparse.RawTextHelpFormatter,
        usage=argparse.SUPPRESS)
    parser.add_argument('-i', required=True, type=str,
                        help=I_FLAG_HELP_TEXT)
    args = parser.parse_args()

    # 2. Make sure Budget roll-up file exists
    if not os.path.exists(args.i):
        raise BudgetFileNotFoundError(
            f"The transformed/cleaned budget file provided "
            f"as input to this script is not found at this location: "
            f"{args.i}"
        )

    df = pd.read_csv(args.i, delimiter=DELIMITER)
    pdb.set_trace()
    pass


if __name__ == '__main__':
    main()
