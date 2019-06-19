import pandas as pd
import pdb


def _trim_space(cell_str):
    return str(cell_str).strip()


def trim_space(row):
    # REF: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.apply.html
    # pdb.set_trace()
    return row.apply(_trim_space)


def remove_dollar(cell_str):
    return float(cell_str.replace("$", "").replace(",", ""))


rule = {
    'common': ['trim_space'],
    'specific':
        {'sal-rate': ['remove_dollar']}
}

data = {
    'dpt':[868, 868, 69],
    'name':['B J SANDIFORD', 'C A WIGFALL', 'A E A-AWOSOGBA'],
    'address':['  DEPARTMENT OF CITYWIDE ADM', 'DEPARTMENT OF CITYWIDE ADM  ', ' HRA/DEPARTMENT OF SOCIAL S '],
    'ttl#':['12702', '12702', '52311'],
    'pc':[' X ',' X', 'A '],
    'sal-rate':['$5.00', '$5.00', '$51,955.00']
}

df = pd.DataFrame(data)
print("Original Dataframe:\n")
print(df)

# https://thispointer.com/pandas-apply-apply-a-function-to-each-row-column-in-dataframe/
# https://stackoverflow.com/q/36213383
# REF: http://jonathansoma.com/lede/foundations/classes/pandas%20columns%20and%20functions/apply-a-function-to-every-row-in-a-pandas-dataframe/
df['sal-rate'] = df['sal-rate'].apply(remove_dollar)
print("\n>===Applied to one column=========\n")
print(df)
print("=========\n")

df2 = df.apply(trim_space, axis=1)
print("\n>===Applied to all columns=========\n")
print(df2)
print("=========\n")

