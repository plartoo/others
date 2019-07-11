"""
Author: Fredy Leon Arenales
Date: June 17, 2019
Description: import and apply data cleansing rules 
"""
import pandas as pd

# Description: Creates a new string-data-type column and assigns the default value = 'N/A'
# Rules that use it: FREDY
# Why do we create it?: For Peru, we don't receive the columns 'Sector', 'Submedia_1', 'Submedia_2' and 'Vehicle'.
# So we create these columns and assign a default value. That way, the structure is ok and the data is ready to be inserted in the table.
def create_new_columns_str(dt,column_names):
    for col in column_names:
        dt[col] ='N/A'
    return dt

# Description: Creates a new numeric-data-type column and assigns the default value = 0
# Rules that use it: FREDY
# Why do we create it?: For Peru, we don't receive the columns 'Sector', 'Submedia_1', 'Submedia_2' and 'Vehicle'.
# So we create these columns and assign a default value. That way, the structure is ok and the data is ready to be inserted in the table.
def create_new_columns_num(dt,column_names):
    for col in column_names:
        dt[col] = 0
    return dt

# Description: Assigns a default value to string-data-type columns that are empty.
# Rules that use it: FREDY
# Why do we create it?: We always work with a default value regardless of the data type.
# This function replaces empty values with 'N/A' for string-data-type columns.
def replace_null_to_NA(dt,column_names):
    for col in column_names:
        dt[col].fillna('N/A', inplace=True)
    return dt

# Description: Assigns a default value to number-data-type columns that are empty.
# Rules that use it: FREDY
# Why do we create it?: We always work with a default value regardless of the data type.
# This function replaces empty values with 0 for number-data-type columns.
def replace_null_to_0(dt,column_names):
    for col in column_names:
        dt[col].fillna(0, inplace=True)
    return dt

# Description: Renames a column name.
# Rules that use it: FREDY
# Why do we create it?: This is the column mapping between the raw and staging tables.
# Short example below:
"""
		INSERT INTO [STG].[RAW_DATA_PER_STG]
           ([ADVERTISER]
           ,[CATEGORY]
           ,[BRAND]
           ,[PRODUCT]
           ,[SECTOR]
           ,[SUBSECTOR]
           ,[MEDIA]
           ,[FORMAT]
           ,[CREATIVE]
           ,[DAYPART]
           ,[TOTAL_DURATION]
           ,[INSERTIONS]
           ,[LOCAL_SPEND]
           ,[GRP]
           ,[YEAR]
           ,[MONTH]
           ,[FULL_DATE]
           ,[SPOT_LENGTH]
           ,[SUBMEDIA_1]
           ,[SUBMEDIA_2]
           ,[NETWORK]
           ,[VEHICLE])
		SELECT [ANUNCIANTE]	[ADVERTISER],
			[ITEM]			[CATEGORY], 
			[MARCA]			[BRAND],
			[PRODUCTO]		[PRODUCT],
            ''				[SECTOR], 
            [CATEGORIA]		[SUBSECTOR],
            [MEDIO]			[MEDIA],
            [TIPO]			[FORMAT],
			[VERSION]		[CREATIVE],
			[BLOQUE]		[DAYPART],
			[SEGUNDOS(T)]	[TOTAL_DURATION],
            [AVISOS]		[INSERTIONS],
			[INVERSION]		[LOCAL_SPEND],
			(CASE medio WHEN 'Cable' THEN [Amas 18-99 Lima(Cable)] ELSE [Amas 18-99 Lima(Tv)] END) [GRP],
			Year			[YEAR],
			Month			[MONTH],
			NULL			[FULL_DATE],
            NULL			[SPOT_LENGTH],
           ''				[SUBMEDIA_1],
           ''				[SUBMEDIA_2],
		   [EMISORA/SITE]	[NETWORK],
			''				[VEHICLE]
		FROM
			[ODS].[RAW_DATA_PER] 
"""
def rename_columns(dt,dic):
    return dt.rename(index=str, columns=dic)

# Description: Deletes a column that we don't need to load into the database.
# Rules that use it: FREDY
# Why do we create it?: We don't need the columns 'DURACION' and 'POSICION'.
def delete_columns(dt,column_names):
    for col in column_names:
        dt.drop(columns =[col], inplace = True) 
    return dt

# Description: Calculates the spot length based on the formula spot_length = duration / insertion.
# Rules that use it: FREDY
# Why do we create it?: We need the column Spot_Length.
def calculate_spot_length(dt,duration,insertion):
    dt['Spot_Length']=dt[duration] / dt[insertion]
    return dt

# Description: Splits the values of a column into two new columns, and deletes the old column.
# Rules that use it: FREDY
# Why do we create it?: The date comes as 'Mayo del 2019'.
# We need a column for the Month, and a column for the Year.
def split_column(dt,col_names,separators,new_col_names):
    for i in range(len(col_names)):
        dtt = dt[col_names[i]].str.split(separators[i], expand = True)
        dic ={dtt.columns[i]:new_col_names[i]}
        rename_columns(dtt,dic)
        delete_columns(dt,[col_names[i]]) 
        create_new_columns_str(dt,new_col_names[i])
        for j in range(len(dtt.columns)):
            dt[new_col_names[i][j]] = dtt[dtt.columns[j]]
    return dt

# Description: Deletes records/rows where a specific column is NULL (similar to a "DELETE FROM TABLE1 WHERE SPEND IS NULL" sentence).
# Rules that use it: FREDY
# Why do we create it?: To eliminate NULL values.
def delete_null(dt,col_names):
    for col in col_names:
        dt=dt[~dt[col].isnull()]
    return dt

# Description: Returns a DataFrame the meets a specific condition.
# Rules that use it: FREDY
# Why do we create it?: Not sure how to implement a generic solution where we can delete records that must meet 2 or more conditions
# (e.g. "DELETE FROM TABLE WHERE MEDIA IN ('TV','Radio') AND SPOT_LENGTH = 0")

# To implement the previous example, we first filter the data using this function and then we delete records using the 2nd condition, which in our example if "SPOT_LENGTH = 0".
# Example with Peru:
# df = isin(dt,['MEDIO'],["RADIO","TV"]) --Data filtered by the 1ast condition
# delete_null(df,['POSICION']) --Deletes data based on the 2nd condition
def isin(dt,col_names,conditions):
    dt = dt[dt[col_names].isin(conditions)]
    return dt

# Similar explanation of the previous function, except it filters the data that doesn't meet a particular condition
# (e.g. "DELETE FROM TABLE WHERE MEDIA NOT IN ('TV','Radio') AND SPOT_LENGTH = 0").
def notin(dt,col_names,conditions):
    dt[~dt[col_names].isin(conditions)]
    return dt    
	

# File name
File= 'PER_N_ALL_ALL_MMU_20190501_20190531_20<190617_JD.xlsx'

# Read the DataFrame from an Excel file with Pandas. We skip the header, which is the first 8 rows.
dt = pd.read_excel(File,skiprows=8) #, encoding='ISO-8859-1')

# Drops all empty columns
dt = dt.loc[:,~dt.columns.str.contains('Unnamed')].dropna(how='all')

# These are rules 1 and 2 from RAW to STG in the Excel file
dt = dt[ dt.DURACION.notnull() ]

# This is rule 3 from RAW to STG in the Excel file
# DataFrame df contains the records for which the column 'MEDIO' is 'RADIO' or 'TV'
df = isin(dt,['MEDIO'],["RADIO","TV"])
# From the DataFrame df, records for which POSICION is 0 are deleted
delete_null(df,['POSICION'])

# This is rule 3
# DataFrame da contains the records for which the column 'MEDIO' is 'CABLE'
da = isin(dt,['MEDIO'],["CABLE"])
# From the DataFrame da, records for which POSICION is 0 are deleted
delete_null(da,['POSICION'])

# DataFrame dt contains the records for which the column 'MEDIO' is NOT 'RADIO', 'CABLE' or 'TV'
dt = notin(dt, ['MEDIO'], ["CABLE","RADIO","TV"])

# The raw file has 4 columns, one with the GRP for TV, another with the GRP for CABLE.
# Since we separated these media into 3 DataFrames, it is necessary to delete the columns that contain GRP for media that isn't in the DataFrame
# For instance, we delete the column that contains GRP for CABLE in the DataFrame that contains only TV
delete_columns(df,['TOTAL','Amas 18-99 Lima(Cable)'])
delete_columns(da,['TOTAL','Amas 18-99 Lima(Tv)'])
delete_columns(dt,['TOTAL','Amas 18-99 Lima(Tv)', 'Amas 18-99 Lima(Cable)'])

# We create the new column Grp to unify all three GRP columns in the raw file
create_new_columns_num(dt,['Grp'])

# This is rule 1
df = df[~df['BLOQUE'].isin(["DAY(06:00-23:59)", "MEDIO DIA(12:00-23:59)", "ROTATIVO(08:00-23:59)"])]
delete_null(df,['BLOQUE'])
da = da[~da['BLOQUE'].isin(["DAY(06:00-23:59)", "MEDIO DIA(12:00-23:59)", "ROTATIVO(08:00-23:59)"])]

# These columns are deleted because they are never imported to the Data Base
delete_null(da,['BLOQUE'])
delete_null(dt,['EMISORA/SITE'])
delete_null(df,['VERSION'])
delete_null(da,['VERSION'])

# This is rule 6
create_new_columns_num(dt,['Spot_Length'])
create_new_columns_num(df,['Spot_Length'])
create_new_columns_num(da,['Spot_Length'])

# This is rule 11
calculate_spot_length(df,'SEGUNDOS(T)','AVISOS')
calculate_spot_length(da,'SEGUNDOS(T)','AVISOS')

# Here we unify all 3 DataFrames, mapping the GRP corresponding columns in each one to the final GRP column we created in line 193 called 'Grp'
dt=pd.concat([dt, da.rename(columns={'Amas 18-99 Lima(Cable)':'Grp'}), df.rename(columns={'Amas 18-99 Lima(Tv)':'Grp'})], sort=True)

# Here we rename all columns with their standard name
dic={"MEDIO": "Media", "TIPO": "Format", "ANUNCIANTE": "Advertiser", "MARCA": "Brand", "PRODUCTO": "Product", "CATEGORIA": "Subsector", "ITEM": "Category", "EMISORA/SITE": "Network", "BLOQUE": "Daypart", "SEGUNDOS(T)": "Total_Duration", "INVERSION": "Local_Spend", "VERSION": "Creative", "AVISOS": "Insertions"}
dt = rename_columns(dt,dic)
# These are rules 5, 7, 8, 9
create_new_columns_str(dt,['Sector','Submedia_1','Submedia_2','Vehicle'])

# These are rules 14 to 21, and 29
replace_null_to_NA(dt,['Advertiser','Category','Brand','Product','Subsector','Daypart','Media','Creative','Network'])

# These are rules 25, 26
replace_null_to_0(dt,['Grp','Local_Spend','Insertions','Total_Duration'])

# These are rules 23, 24
dt.replace({'Insertions': 'N/A', 'Total_Duration': 'N/A'}, 0)

# This is done in the raw table
split_column(dt,['MES'],['del'],[['Month','Year']])

# We delete columns DURACION and POSICION, which we don't import to the Data Base
delete_columns(dt,['DURACION','POSICION']) 

# We save the DataFrame in a csv file
dt.to_csv('PER_Cleaned_File.csv', index=False, sep='|',decimal='.', encoding='utf-8')

print(dt)

