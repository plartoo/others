import glob
import os
import re

import pandas as pd

file_location = 'C:/Users/lache/Desktop/US'
files_to_convert = glob.glob(os.sep.join([os.path.normpath(file_location),'*.xlsx']))
non_temp_files = [f for f in files_to_convert if re.match(r'[^~]*.xlsx',f)]

# sheet_names = ['TV', 'Radio', 'Magazine', 'Newspaper', 'Online Display', 'Online Video']
sheet_names = ['Newspaper', 'Online Display', 'Online Video']
essential_cols = {'CATEGORY', 'SUBCATEGORY', 'PARENT', 'ADVERTISER', 'BRAND', 'PRODUCT', 'MEDIA', 'DATE', 'DOLS'}
all_cols_to_drop = {'TITLE', 'MARKET', 'TIME', 'EDITION', 'PAGE #', 'ZONE'}

for sn in sheet_names:
    frames = []

    for f in non_temp_files:
        print(f"Processing: {f}, Sheet name:{sn}")
        df = pd.read_excel(f
                           ,
                           sheet_name=sn,
                           header=7,#5,
                           # skiprows=7,
                           skipfooter=3
                           )
        cols_to_drop = set(df.columns).intersection(all_cols_to_drop)
        print(f"These columns will be dropped: {cols_to_drop}")
        # import pdb; pdb.set_trace()
        df = df.drop(cols_to_drop, axis=1)

        if 'MEDIA' not in df.columns:
            df['MEDIA'] = sn

        if (not df.empty) and (set(df.columns) == essential_cols):
            df = df[['CATEGORY', 'SUBCATEGORY', 'PARENT', 'ADVERTISER', 'BRAND', 'PRODUCT', 'MEDIA', 'DATE', 'DOLS']]
            frames.append(df)

    combined_df = pd.concat(frames)
    outfile_name = ''.join([os.path.splitext(file_location)[0], '_', sn, '.csv'])
    combined_df.to_csv(outfile_name, sep='|', index=False)
    print(f"Combined dataframes written to: {outfile_name}")
