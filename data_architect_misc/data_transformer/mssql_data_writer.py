from datetime import datetime
import os
import urllib

import pandas as pd
from sqlalchemy import create_engine

import transform_utils


class MSSQLDataWriter:
    """
    This class the parent class of DataWriter, which is required
    to write data from Pandas dataframe to a new Microsoft SQL
    table. If a table with the same name as the destination table
    already exist in the database,  an error will be thrown.
    """
    def __init__(self, config):
        # We can later implement other pandas.to_excel parameters
        # such as na_rep, columns, header, etc.
        self.output_file_path_and_name = self.get_output_file_path_and_name(config)
        self.include_index = self.get_include_index_column_in_output_excel_file(config)
        # Encoding of the resulting excel file.
        # Only necessary for xlwt, other writers support unicode natively.
        self.output_file_encoding = self.get_output_excel_file_encoding(config)
        self.sheet_name = self.get_output_excel_file_sheet_name(config)


    @staticmethod
    def get_output_file_path_and_name(config):
        """
        Returns output file path with file name prefix, if the latter
        is provided in the config JSON. Before joining the path with
        file name, output folder is created if it doesn't exist already.
        """
        output_folder = transform_utils.get_output_folder(config)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print("\nINFO: new folder created for output files =>", output_folder)

        file_prefix = transform_utils.get_output_file_prefix(config)
        file_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file_name = ''.join(['_'.join([file_prefix, file_suffix]), '.xlsx'])

        return os.path.join(output_folder, output_file_name)


    @staticmethod
    def get_include_index_column_in_output_excel_file(config):
        """
        Extracts and return boolean value to decide if output Excel
        file should include index column from the dataframe.
        """
        return transform_utils.get_include_index_column_in_output_file(config)


    @staticmethod
    def get_output_excel_file_encoding(config):
        """
        Extracts and return encoding string value for output Excel file.
        Defaults to None because it is (strangely) equivalent to 'utf-8'
        in Pandas.
        """
        return transform_utils.get_output_file_encoding(config)


    @staticmethod
    def get_output_excel_file_sheet_name(config):
        """
        Extracts and return sheet name (string) for output Excel file.
        Defaults to None because it is (strangely) equivalent to 'utf-8'
        in Pandas.
        """
        return transform_utils.get_output_file_sheet_name(config)


class DataWriter(MSSQLDataWriter):
    """
    This class is the child class of MSSQLDataWriter.
    Anyone who wants to implement other custom DataWriter class
    must make sure that it implements write_data(dataframe) method
    because it is expected in transform.py file.
    """

    def __init__(self, config):
        super().__init__(config)


    def create_sqlalchemy_engine(self, url_of_sql_server):
        """
        Although the following references (1, 2, 3, 4) are good to read,
        they, in practice, didn't work as well as a comment on StackOverflow
        in defining what string value to pass to create sqlalchemy engine
        as well as how to pass in database schema name in 'to_sql'.
        REF: https://stackoverflow.com/a/36531779/1330974

        REF 1: https://docs.sqlalchemy.org/en/13/core/engines.html [http://archive.ph/bf4fv]
        http://web.archive.org/web/20200325020538/https://docs.sqlalchemy.org/en/13/core/engines.html

        REF 2: https://docs.sqlalchemy.org/en/13/dialects/mssql.html [http://archive.ph/wip/WNhTq]
        http://web.archive.org/web/20200325020718/https://docs.sqlalchemy.org/en/13/dialects/mssql.html

        REF 3: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html [http://archive.ph/wip/T6vJk]
        http://web.archive.org/web/20200325020822/https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html

        REF 4: https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#engine-connection-examples
        https://web.archive.org/web/20200325023532/https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html

        :param url_of_sql_server:
        :return:
        """
        # import sqlalchemy
        # import pandas as pd
        # import urllib
        # server = "wm-rf-svr-colgate.database.windows.net"
        # database = "WM_RF_DB_Colgate"
        # user = "wm-rf-svr-usr-colgate"
        # password = ""
        # df = pd.DataFrame({'name': ['User 1', 'User 2', 'User 3']})
        # engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect={}".format(urllib.parse.quote_plus(
        #     "DRIVER=ODBC Driver 13 for SQL Server;SERVER={0};PORT=1433;DATABASE={1};UID={2};PWD={3};TDS_Version=8.0;;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(
        #         server, database, user, password))), echo=False)
        # df.to_sql(name='test', con=engine, if_exists='replace', schema='dbo')
        pass

    def write_data(self, df):
        print("Writing data to:", self.output_file_path_and_name)
        df.to_excel(
            self.output_file_path_and_name,
            sheet_name=self.sheet_name,
            index=self.include_index,
            encoding=self.output_file_encoding
        )
