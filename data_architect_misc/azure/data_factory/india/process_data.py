"""
Author: Jholman
Date: March 6, 2019
Description: Cleaning procedure for two different file formats for India. (more explanation here if relevant)
"""
import pandas as pd


def process_data(file_name):
    melt_columns = ['Advertiser', 'Section', 'Category', 'Product']
    dt = pd.read_excel(file_name, skiprows=5)##Skip the first 5 rows related to headers
    dt = dt.drop(index = [1, 2, 3]).reset_index(drop = True)
    ##This expression add accordinly to the leftmost spaces in the first column; categorize them based on that spaces (Advertiser = 0 spaces, Section = 1 spaces, Category = 2 spaces, Product = 3 spaces)
    dt.loc[:,'Advertiser'] = dt['MAP 3.5 - Media Analysis'].fillna('').apply(lambda x: str(x).lstrip() if len(str(x)) - len(str(x).lstrip()) == 0 else None)
    dt.loc[:, 'Section'] = dt['MAP 3.5 - Media Analysis'].fillna('').apply(lambda x: str(x).lstrip() if len(str(x)) - len(str(x).lstrip()) == 1 else None)
    dt.loc[:, 'Category'] = dt['MAP 3.5 - Media Analysis'].fillna('').apply(lambda x: str(x).lstrip() if len(str(x)) - len(str(x).lstrip()) == 2 else None)
    dt.loc[:, 'Product'] = dt['MAP 3.5 - Media Analysis'].fillna('').apply(lambda x: str(x).lstrip() if len(str(x)) - len(str(x).lstrip()) == 3 else '')

    dt.drop(columns = 'MAP 3.5 - Media Analysis',inplace = True, axis = 1)#Delete row not needed to show in the process axis = 1 = delete the Colum named 'MAP 3.5 - Media Analysis'
    ##Transform the empty columns adding the previous values to add the date to empty field
    dt.columns = pd.Series(dt.columns).apply(lambda x: None if 'Unnamed' in x else x).fillna(method='ffill')
    dt = dt.fillna(method='ffill')#fill colums empty with the previous data
    ##Merge media data to the date before the unpivot
    dt.columns = [str(x) if str(x)=='Advertiser' or str(x)=='Section' or str(x)=='Category' or str(x)=='Product'  else  str(x) + '_' + str(y) for x, y in dt[0:1].squeeze().iteritems()]
    dt = dt[dt['Product'] != '']
    ##Melt or unpivot dataframe table
    dt = pd.melt(dt, id_vars = melt_columns, var_name = 'Date_Media', value_name = 'Spend')

    #Split date_media columns to Media and data columns
    dt.loc[:,'Media'] = dt['Date_Media'].apply(lambda x:x.split('_')[1])
    dt.loc[:,'Date'] = dt['Date_Media'].apply(lambda x:x.split('_')[0].replace("'",""))
    dt.drop(columns='Date_Media', inplace=True, axis=1) ##Rop column named date_Media
    return dt
