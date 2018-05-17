import argparse
import csv
import pprint
pp = pprint.PrettyPrinter(indent=4)
import sys

import account_info
import queries
from sql_server_utils import SqlServerUtils
from data_writer import DataWriter


def get_country_metadata():
    db = SqlServerUtils(account_info.DM_1219)
    data = db.fetch_all_data(queries.country_metadata)
    print("Retrieved metadata from CP_COUNTRY_DIM table....")
    return {row[1]: dict(zip(data[0], row)) for row in data[1:]}


def prepare_fact_queries_and_output_configs(countries, country_metadata):
    q = []
    for c in countries:
        if c in country_metadata:
            fact_query_and_output_config = queries.get_fact_query(country_metadata[c])
            fact_query_and_output_config['split_file'] = True
            # fact_query_and_output_config['split_by'] = 'row' # alternative is 'size'
            # fact_query_and_output_config['split_limit'] = ROW_COUNT # for 'size', provide integer as file size in MB
            fact_query_and_output_config['split_by'] = 'size' # alternative is 'size'
            fact_query_and_output_config['split_limit'] = 190 # for 'size', provide integer as file size in MB
            fact_query_and_output_config['quoting'] = csv.QUOTE_NONE # CBS does NOT want double quotes
            q.append(fact_query_and_output_config)
        else:
            sys.exit('\n***!!! WARNING: [COUNTRY_KEY] is not found in the [CP_DIM_COUNTRY] => ' + c)
    return q


if __name__ == '__main__':
    ROW_COUNT = 1500000

    # REF: https://stackoverflow.com/a/30493366
    parser = argparse.ArgumentParser(description='Generate key figure (fact and dimension) files')
    parser.add_argument('countries',
                        type=str,
                        help='List of comma-separated country keys such as ARG,HKG,GRE.')
    args = parser.parse_args()
    countries = args.countries.split(',')
    print('List of countries provided: ', countries)

    country_metadata = get_country_metadata()
    fact_queries = prepare_fact_queries_and_output_configs(countries, country_metadata)
    print("\n===> List of queries and their configurations to be run <===")
    pp.pprint(fact_queries + queries.dim_queries)

    writer = DataWriter()
    db = SqlServerUtils(account_info.DM_1219)

    for q in fact_queries:
        print("\n===> Generating FACT file using the query and config below:")
        pp.pprint(q)
        writer.write_data_incrementally(db.get_connection(), q)

    for q in queries.dim_queries:
        print("\n===> Generating Dimension file using the query and config below:")
        pp.pprint(q)
        writer.write_data_all_at_once(db.fetch_all_data(q['query']), q)
    print('\n###Key figure file generation completed.###')
