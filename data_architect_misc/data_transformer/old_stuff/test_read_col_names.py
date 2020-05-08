import pdb
import transform_errors
import transform_utils

if __name__ == '__main__':
    config = {
        'row_index_to_extract_column_names': 0,
        'input_csv_file_delimiter': '|',
        #'custom_column_names_to_assign': ['a','b'],
    }
    print(transform_utils.get_raw_column_names('csv_n.csv', config))

    config = {
        'row_index_to_extract_column_names': 4,
        'input_csv_file_delimiter': '|',
        #'custom_column_names_to_assign': ['a','b'],
    }
    print(transform_utils.get_raw_column_names('csv_d.csv', config))

    config = {
        'row_index_to_extract_column_names': 4,
        'input_csv_file_delimiter': '|',
        'custom_column_names_to_assign': ['a','b'],
    }
    print(transform_utils.get_raw_column_names('csv_d.csv', config))

    config = {
        'row_index_to_extract_column_names': 0,
        'input_csv_file_delimiter': '|',
    }
    print(transform_utils.get_raw_column_names('excel_n.xlsx', config))

    config = {
        'row_index_to_extract_column_names': 4,
        'input_csv_file_delimiter': '|',
    }
    print(transform_utils.get_raw_column_names('excel_d.xlsx', config))

    config = {
        'row_index_to_extract_column_names': 4,
        'input_csv_file_delimiter': '|',
        'custom_column_names_to_assign': ['a','b'],
    }
    print(transform_utils.get_raw_column_names('excel_d.xlsx', config))

    # df2=pd.read_csv('csv_d.csv',delimiter='|', skiprows=4, nrows=0)
    # df3=pd.read_excel('excel_n.xlsx', sheet_name=0, header=0, nrows=0)
    # df3=pd.read_excel('excel_d.xlsx', sheet_name=0, header=4, nrows=0)

