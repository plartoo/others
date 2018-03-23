import argparse

import pdb
import pprint
pp = pprint.PrettyPrinter(indent=4)

import account_info
import queries
from sql_server_utils import SqlServerUtils

def get_country_metadata():
    db = SqlServerUtils(account_info.DM_1219)
    data = db.fetch_all_data(queries.country_metadata)
    return {row[1]: dict(zip(data[0], row)) for row in data[1:]}


if __name__ == '__main__':
    # REF: https://stackoverflow.com/a/30493366
    parser = argparse.ArgumentParser(description='Generate key figure (fact and dimension) files')
    parser.add_argument('countries',
                        type=str,
                        help='List of comma-separated country keys such as ARG,HKG,GRE.')
    args = parser.parse_args()
    countries = args.countries.split(',')
    print('List of countries provided: ', countries)

    country_metadata = get_country_metadata()

    for c in countries:
        if c in country_metadata:
            print('\nGenerating fact file(s) for this country:', c)
            c_metadata = country_metadata[c]
            pp.pprint(c_metadata)
        else:
            print('\n**** WARNING: country name is not found in our metadata table =>', c)

    print('\nKey figure file generation completed.')
