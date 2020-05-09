from _functools import partial
import pandas as pd

class TransformFunctions(object):
    # def _trim_space(self, cell_str):
    #     return str(cell_str).strip()

    # def trim_space(row):
    #     # this is where we need to create a private method to apply to each cell
    #     # REF: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.apply.html
    #     # pdb.set_trace()
    #     return row.apply(_trim_space)


    def trim_space(self, row):
        # This is just an example of plain old trim_space applied to the whole row
        # REF: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.apply.html
        return row.str.strip()


    def remove_dollar_with_additional_arg(self, cell_str, additional_arg):
        print()
        print(cell_str, "\t", additional_arg)
        return float(cell_str.replace("$", "").replace(",", ""))


    def remove_dollar(self, cell_str):
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

klass = TransformFunctions()
# df['sal-rate'] = df['sal-rate'].apply(getattr(klass,'remove_dollar'))
# to pass additional parameters, do this: https://stackoverflow.com/a/56675539/1330974
remove_dollar_with_additional_arg = partial(getattr(klass,'remove_dollar_with_additional_arg'),
                                            additional_arg='test additional argument')
df['sal-rate'] = df['sal-rate'].apply(remove_dollar_with_additional_arg)
print("\n>===Applied to one column=========\n")
print(df)
print("=========\n")

# df2 = df.apply(trim_space, axis=1)
# print("\n>===Applied to row aka all columns=========\n")
# print(df2)
# print("=========\n")


## This is how we would do it if the functions aren't wrapped in TransformFunctions class
# # https://thispointer.com/pandas-apply-apply-a-function-to-each-row-column-in-dataframe/
# # https://stackoverflow.com/q/36213383
# # REF: http://jonathansoma.com/lede/foundations/classes/pandas%20columns%20and%20functions/apply-a-function-to-every-row-in-a-pandas-dataframe/
# df['sal-rate'] = df['sal-rate'].apply(remove_dollar)
# print("\n>===Applied to one column=========\n")
# print(df)
# print("=========\n")
#
# df2 = df.apply(trim_space, axis=1)
# print("\n>===Applied to row aka all columns=========\n")
# print(df2)
# print("=========\n")

