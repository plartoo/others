import pypyodbc

class SqlServerUtils(object):

    def __init__(self, server_info):
        """
        A wrapper class to create connection, cursor, run queries and fetch data
        from SQL Server database.

        :param server_info: A string representing all log-in information to the database server.
            For example:
            "Driver={SQL Server};Server=ipAndPort;Database=DatabaseName;UID=userId;PWD=password;"
        """
        self.server_info = server_info
        self.connection = pypyodbc.connect(server_info)

    def run_query(self, query):
        """
        Run the SQL query string, but no output will be captured.

        :param query: A query string. For example,
            "SELECT * FROM MyTable;"
        """
        cursor = self.connection.cursor()
        cursor.execute(query) # REF: https://stackoverflow.com/a/40404653
        cursor.close()

    def fetch_all_data(self, query):
        """
        Run the SQL query string, and fetch ALL the data returned by that query.

        :param query: A query string. For example,
            "SELECT * FROM MyTable;"

        :return: Data in the table in Python List format.
        """
        cursor = self.connection.cursor()
        cursor.execute(query) # REF: https://stackoverflow.com/a/40404653
        headers = [[header[0] for header in cursor.description]]
        data = headers + [list(row) for row in cursor.fetchall()] # REF: https://github.com/jiangwen365/pypyodbc/
        cursor.close()

        return data

    def get_connection(self):
        """
        Return connection class variable if user wants to create a cursor and
        browse the database tables manually.
        :return:
        """
        return self.connection

    def close_connection(self):
        """
        Close the database connection.
        If unsure about '__del__' method closing the connection, use this.
        """
        self.connection.close()

    def __del__(self):
        """
        Ensures that we always close the database connection.
        If concerned about this 'evil' practice of using destructor in Python, please read:
        https://web.archive.org/web/20180313171600/https://eli.thegreenplace.net/2009/06/12/safely-using-destructors-in-python
        """
        if self.connection:
            print("Database connection closed.")
            self.connection.close()




