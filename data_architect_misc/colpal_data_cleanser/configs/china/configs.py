configs = [
    {
        'input_file_path': '', # optional; we can default this
        'input_file_name': '', # pattern is okay
        'leading_rows_to_skip': 0, # we can default this
        'trailing_rows_to_skip': 0, # we can default this
        'indexes_of_columns_to_drop': [], #dfObj.drop(['Age' , 'Name'] , axis='columns', inplace=True) or df.drop(df.columns[[1,2,4,5,12]],axis=1,inplace=True) where index is 0 based
        'names_of_columns_to_drop': [],
        'functions_to_apply_to_columns': {
            'column1': [],
            'column2': [],
        },
        'functions_to_apply_to_rows': [],
        'column_rename_mappings': {},
        'output_file_path': '', # optional; we can create a default. we must check if it exists, if not, create one
        # 'new_columns_to_add': [{'new_column': ['rules_used_to_populate_this_column']}],
        # 'qa': '?', # data type verification etc.
    }
]
