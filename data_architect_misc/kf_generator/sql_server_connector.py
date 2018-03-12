import pdb

from account_info import SERVER_INFO_STR
import pypyodbc

import pprint
pp = pprint.PrettyPrinter(indent=4)

conn = pypyodbc.connect(SERVER_INFO_STR)
cursor = conn.cursor()
query = "SELECT * FROM [DM_1219_ColgateGlobal].[CLI].[Product_CRF_ARG]"

cursor.execute(query) # REF: https://stackoverflow.com/a/40404653
# data = cursor.fetchone()
# while data:
#     pdb.set_trace()
#     print(str(data[0]) + ", " + ... + ", " + str(data[n-1]))
#     data = cursor.fetchone()

# REF: https://github.com/jiangwen365/pypyodbc/
columns = [column[0] for column in cursor.description]
pp.pprint(columns)
ddd = cursor.fetchall()
pdb.set_trace()
# for row in cursor.fetchall():
#     pp.pprint(dict(zip(columns, row)))

cursor.close()
conn.close()

# python generate_kf.py HK
#
#
# queries/

