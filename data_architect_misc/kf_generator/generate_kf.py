import pdb
import pprint
pp = pprint.PrettyPrinter(indent=4)

from account_info import SERVER_INFO_STR
from sql_server_utils import SqlServerUtils

db = SqlServerUtils(SERVER_INFO_STR)
query = "SELECT * FROM [DM_1219_ColgateGlobal].[CLI].[Product_CRF_USA]"
data = db.fetch_all_data(query)

print('done')
