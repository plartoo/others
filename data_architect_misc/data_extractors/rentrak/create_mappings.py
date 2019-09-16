"""
Author: Phyo Thiha
Last Modified: September 13, 2019
Description: This scripts extracts national network names and corresponding short names
from Network Monthly Trend (national rating) files. It then extracts individual network
names from Market Monthly Trend files. Then it uses fuzzy string matching algorithm
to guess which network name in Market Monthly Trend files corresponds to which entries
in national rating.

IMPORTANT NOTE: The output of this script must be manually reviewed by a person
(not robot/computer) to make sure the mappings are correct. Because the fuzzy
string matching is not going to make 100% accurate mappings.
"""

from datetime import datetime
import re
import os

import pandas as pd
from fuzzywuzzy import fuzz


# TODO: refactor PLACEHOLDER to another file that can be used by both create_mappings and calculate_indexes
# Placeholder keyword used when we cannot find matching national network (short) names
PLACEHOLDER = 'Not Available'

# Folder where Network Monthly and Market Monthly files lives
DATA_FOLDER = os.path.join(os.getcwd(), 'selenium_output')

# Mapping (output) file name
cur_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
MAPPING_FILE = os.path.join(DATA_FOLDER, ''.join(['network_mappings_', cur_datetime, '.csv']))
national_rating_files = [os.path.join(DATA_FOLDER,f) for f in os.listdir(DATA_FOLDER)
                         if (os.path.isfile(os.path.join(DATA_FOLDER, f)) and 'Network_Monthly_Trend' in f)]
market_rating_files = [os.path.join(DATA_FOLDER,f) for f in os.listdir(DATA_FOLDER)
                       if (os.path.isfile(os.path.join(DATA_FOLDER, f)) and 'Market_Monthly_Trend' in f)]

national_networks = {}
for f in national_rating_files:
    df = pd.read_excel(f, na_values="-", index_col=0, skiprows=5, skipfooter=6)
    print("Loading national network names along with their short names from...", f)
    # The national network names vary year over year from ~270 to ~250
    for nname in df.index:
        short_name = re.findall(r'\((.*?)\)', nname)[-1]
        national_networks[nname] = short_name

market_networks = {}
for f in market_rating_files:
    df = pd.read_excel(f, nrows=1, skiprows=2)
    print("Loading market network names from...", f)
    # There are 300 individual networks as of September 2019.
    market_network_name = df.columns[0].split(',')[0].strip()
    market_networks[market_network_name] = 0

mappings = []
for market_network, _ in market_networks.items():
    print("Mapping market networks to national networks using fuzzy matching for market network:", market_network)
    highest_match_percent = 0
    highest_matched_national_network = ''
    highest_matched_national_network_short_name = ''
    for national_network, shortname in national_networks.items():
        national_no_paren = re.search(r'(.*?)\(', national_network)[1].strip()
        cur_match_percent = fuzz.ratio(market_network.strip().lower(), national_no_paren.lower())
        if cur_match_percent > highest_match_percent:
            highest_match_percent = cur_match_percent
            highest_matched_national_network = national_network
            highest_matched_national_network_short_name = shortname
    if highest_match_percent < 70:
        # if the matching ratio is lower than 70 percent, we assume there is no mapping available for this market network
        mappings.append([market_network, PLACEHOLDER, PLACEHOLDER])
    else:
        mappings.append([market_network, highest_matched_national_network, highest_matched_national_network_short_name])

df = pd.DataFrame(mappings, columns=["Market Network Names", "National Network Names", "National Network Short Names"])
df.to_csv(MAPPING_FILE, index=False, encoding='utf-8')
print("Market networks mapped to national networks and are placed int the file:", )
