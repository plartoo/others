import logging
import urllib

from sqlalchemy import create_engine

import transform_utils


class DBSchemaNotDefinedError(Exception):

    """Raised when database schema is not defined
    (is empty string) in the config file.
    """
    def __str__(self):
        return f"ERROR: {self.args}"


class MSSQLDataWriter:
    PYODBC_BASE_URL = "mssql+pyodbc:///?odbc_connect={}"
    # Note: feel free to adjust other parameters below as needed
    OTHER_URL_PARAMS = "TDS_Version=8.0;;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

    # Below are default values for other parameters for pandas dataframe.to_sql method.
    # To keep parameters/options simple, I have decided to not integrate them as JSON
    # config file parameters in transform.py, and opted to use them as default
    # CONSTANT values in this mssql_data_writer.py module instead.
    # REF: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
    REPLACE_IF_EXISTS = 'fail' # err on the side of throwing error rather than overwriting an existing table

    # We will NOT be using CHUNK_SIZE and METHOD in the end because
    # they are still throwing SQL Alchemy Error that varies based
    # on the chunk size, and I'm not that excited about using this
    # to_sql method, which seems to be not only slow, but too buggy.
    # Also, if chunksize is not provided as parameter, all rows will
    # be loaded at once, and based on some experiments below, that
    # approach is better for us.
    # CHUNKSIZE = None, METHOD = None => 850 secs
    # CHUNKSIZE = 100, METHOD = None => 892 secs
    # CHUNKSIZE = 10000, METHOD = None => 875 secs
    CHUNK_SIZE = None
    # 'multi' means passing multiple values in a single INSERT clause
    # and in practice, it is throwing the errors as shown below.
    # I think Pandas and/or SQL Alchemy needs to sort out these glitches.
    # REF: https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#insertion-method
    # CHUNKSIZE = None, METHOD = 'multi' => sqlalchemy.exc.ProgrammingError: (pyodbc.ProgrammingError) ('The SQL contains 4184 parameter markers, but 331864 parameters were supplied', 'HY000')
    # CHUNKSIZE = 100, METHOD = 'multi' => sqlalchemy.exc.ProgrammingError (pyodbc.ProgrammingError) ('42000', '[42000] [Microsoft][ODBC Driver 13 for SQL Server][SQL Server]Error converting data type nvarchar to bigint. (8114) (SQLExecDirectW)')
    # CHUNKSIZE = 10000, METHOD = 'multi' => sqlalchemy.exc.ProgrammingError: (pyodbc.ProgrammingError) ('The SQL contains -1072 parameter markers, but 130000 parameters were supplied', 'HY000')
    METHOD = 'multi' # to pass multiple values in a single INSERT clause (for better efficiency)


    def __init__(self, config):
        """
        This class the parent class of DataWriter, which is required
        to write data from Pandas dataframe to a new Microsoft SQL
        table.

        NOTE: In order to prevent SQL Server info from leaking,
        user of this class needs to create 'sql_server_account_info.py'
        file with a Python dictionary holding 'driver','server',
        'database', 'driver', 'user_id', 'password' to construct
        hostname-based PYODBC connection string for MS SQL Server
        as mentioned in online SQL Alchemy documentation
        (for example,
        https://docs.sqlalchemy.org/en/13/dialects/mssql.html#module-sqlalchemy.dialects.mssql.pyodbc
        or http://archive.ph/wip/lpsqN
        or https://web.archive.org/web/20200325171111/https://code.google.com/archive/p/pyodbc/wikis/ConnectionStrings.wiki
        ). An example sql_server_info dictionary would be like this:
        sql_server_info = {
            "protocol": "mssql+pyodbc://",
            "user_id": "mydbid",
            "password": "mypassword",
            "server": "mydbserver",
            "port": "1433",
            "database": "mydb",
            "driver": "ODBC Driver 13 for SQL Server",
        }
        """
        from sql_server_account_info import sql_server_info
        self.driver = sql_server_info['driver']
        self.server = sql_server_info['server']
        self.port = sql_server_info['port']
        self.database = sql_server_info['database']
        self.user_id = sql_server_info['user_id']
        self.password = sql_server_info['password']

        self.output_sql_table_name = self.get_output_sql_table_name(config)
        self.db_schema = self.get_database_schema(config)
        # We can implement other to_sql parameters like 'dtype' later
        self.include_index = self.get_include_index_column_in_output_mssql_table(config)


    @staticmethod
    def get_database_schema(config):
        """
        Returns output DB schema name provided in JSON config file.
        If not provided (that is, empty string), throws DBSchemaNotDefinedError.
        """
        if not transform_utils.get_database_schema(config):
            err_msg = f"Database schema must be defined in JSON config file " \
                      f"to write transformed data to SQL table."
            raise DBSchemaNotDefinedError(err_msg)

        return transform_utils.get_database_schema(config)


    @staticmethod
    def get_output_sql_table_name(config):
        """
        Returns output SQL table name provided in JSON config file.
        If not provided, defaults to the name defined in
        'transform_utils.py'.
        """
        return transform_utils.get_output_sql_table_name(config)


    @staticmethod
    def get_include_index_column_in_output_mssql_table(config):
        """
        Extracts and return boolean value to decide if output Excel
        file should include index column from the dataframe.
        """
        return transform_utils.get_include_index_column_in_output(config)


class DataWriter(MSSQLDataWriter):
    """
    This class is the child class of MSSQLDataWriter.
    Anyone who wants to implement other custom DataWriter class
    must make sure that it implements write_data(dataframe) method
    because it is expected in transform.py file.
    """

    def __init__(self, config):
        """
        This class is taking 'config' as the input parameter
        in which user can define parameters such as
        'name', 'schema', 'if_exists', 'index', 'chunksize',
        'method' from pandas to_sql method.
        REF: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
        """
        super().__init__(config)
        self.logger = logging.getLogger(__name__)


    def __get_sqlalchemy_engine(self):
        """
        Create and return SQL Alchemy engine from hostname-based
        PYODBC connection string for MS SQL Server.

        Although the following references (1, 2, 3, 4) are good to read,
        they, in practice, didn't work as well as a comment (REF#0 below)
        on StackOverflow that explains how to define what string value
        to pass to create sqlalchemy engine and how to pass database
        schema name in pandas 'to_sql' method.
        REF 0: https://stackoverflow.com/a/36531779/1330974

        REF 1: https://docs.sqlalchemy.org/en/13/core/engines.html [http://archive.ph/bf4fv]
        http://web.archive.org/web/20200325020538/https://docs.sqlalchemy.org/en/13/core/engines.html

        REF 2: https://docs.sqlalchemy.org/en/13/dialects/mssql.html [http://archive.ph/wip/WNhTq]
        http://web.archive.org/web/20200325020718/https://docs.sqlalchemy.org/en/13/dialects/mssql.html

        REF 3: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html [http://archive.ph/wip/T6vJk]
        http://web.archive.org/web/20200325020822/https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html

        REF 4: https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#engine-connection-examples
        https://web.archive.org/web/20200325023532/https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html
        """

        pyodbc_connection_str = self.PYODBC_BASE_URL.format(urllib.parse.quote_plus(
            "DRIVER={0};SERVER={1};DATABASE={2};PORT={3};UID={4};PWD={5};{6}".format(self.driver,
                                                                                     self.server,
                                                                                     self.database,
                                                                                     self.port,
                                                                                     self.user_id,
                                                                                     self.password,
                                                                                     self.OTHER_URL_PARAMS)))
        return create_engine(pyodbc_connection_str, echo=False)


    def write_data(self, df):
        """
        Write Pandas dataframe as a table in MS SQL Server database
        using Pandas' to_sql method.

        WARNING: Do NOT write data directly to SQL Server table because
        it is painfully slow. For example, to write ~25K rows of 13
        mostly string type (no more than 20 chars in each column)
        columns, it takes ~15 minutes to finish.
        """
        self.logger.info(
            f"Writing data to MSSQL at (server; database; schema; table): "
            f"{self.server}; {self.database}; {self.db_schema}; "
            f"{self.output_sql_table_name}")

        df.to_sql(
            name=self.output_sql_table_name,
            con=self.__get_sqlalchemy_engine(),
            schema=self.db_schema,
            if_exists=self.REPLACE_IF_EXISTS,
            index=self.include_index,
            # chunksize=self.CHUNK_SIZE,
            # method=self.METHOD
        )

# For future reference in other projects:
# A way to READ MSSQL data via pandas
# >>> sql_conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=;DATABASE=;UID=;PWD=;')
# df1 = pd.read_sql("select top 100 * from dbo.bra", sql_conn)
