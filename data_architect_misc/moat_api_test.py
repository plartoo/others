import base64
import json
import urllib.request

import pdb

def stringToBase64(s):
    """
    Transform string to utf-8 bytecode because that's what MOAT API wants our username and pwd to be converted to.
    """
    return base64.b64encode(bytes(s, 'utf-8'))

username = 'nestle_us_display@moat.com'
password = 'PasswordHere'
url = 'https://api.moat.com/1/stats.json?start=20180114&end=20180131&columns=level1,impressions_analyzed,in_view_percent,active_in_view_time,universal_interactions_percent,clicks_percent'

req = urllib.request.Request(url)
usr_pwd = '{}:{}'.format(username, password).replace('\n', '')
# below, we need to convert base64 string back to regular string before adding this as header value in HTML request
base64string = str(stringToBase64(usr_pwd), 'utf-8')
# now, we prepare HTML header for this request
req.add_header("Authorization", 'Basic {}'.format(base64string))
result = urllib.request.urlopen(req)

try:
    result = urllib.request.urlopen(req)
except urllib.error.URLError:
    print('URL did not work')

# the data below is returned as a byte string
result_bytes = result.read()

# therefore, first we need to decode those UTF-8 bytes to Unicode
result_str = result_bytes.decode('utf8')

# second, load the str as a Python dictionary
result_json = json.loads(result_str)

# (optional) you can even dump it out as a formatted JSON string to print in stdout as prettified format
s = json.dumps(result_json, indent=4, sort_keys=True)
print(s)

# below, you can do whatever you want with this such as writing the above JSON data to a CSV file or whatnot