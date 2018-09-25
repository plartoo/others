import argparse
import os.path

import pandas as pd

if __name__ == '__main__':
    desc = """
    Script to unpivot the data in an excel file when list of columns to unpivot are provided.
    Example usage:
    > python unpivot.py -i "DS001i_Spend_SOS_TW_201802 to 201804_Cleaned.xlsx" -c "2018/02" "2018/03"
    will unpivot the "2018/02" and "2018 01" columns in the input file.
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-c', type=str, required=True,
                        nargs='*',
                        help='List of columns to unpivot. E.g., "Date 1" "Date 2" "Date3"')
    parser.add_argument('-i', type=str, required=True,
                        help='Input Excel files that has data to pivot')
    args = parser.parse_args()

    cols_to_unpivot = args.c
    file_in = args.i
    file_in_name = os.path.splitext(file_in)[0]
    file_extension = os.path.splitext(file_in)[1]
    file_out = file_in_name + '_unpivoted' + file_extension

    df = pd.read_excel(file_in)
    raw_cols = df.columns

    primary_cols = [c for c in raw_cols if c not in cols_to_unpivot]

    df_pivoted = pd.melt(df,
                         id_vars=primary_cols,
                         value_vars=cols_to_unpivot)

    df_pivoted.to_excel(file_out, index=False)
    print("Unpivoted file written at:", file_out)


