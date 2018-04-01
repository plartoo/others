import pdb
import csv
import os.path
import pprint
pp = pprint.PrettyPrinter(indent=4)


# GM_CATEGORY cannot belong to >1 CP_SUBCAT
# GM_PRODUCT_NAME cannot belong to >1 GM_CATEGORY
# Under each country, collect data
# under each group of country data,
# COUNTRY => {GM_PRODUCT_NAME_x => { GM_CATEGORY_NAME  => CP_SUBCATEGORY => row

def load_mappings(filename):
    cur_dir_path = os.path.dirname(os.path.realpath(__file__))
    url_file = os.path.join(cur_dir_path, filename)
    data = {}
    row_cnt = 0
    with open(url_file, 'r') as csvfile:
        for row in csv.reader(csvfile):
            row_cnt +=1
            if row_cnt == 1:
                header = row
                print(header,"\n\n")
            else:
                country = row[3]
                gm_prod = row[9]
                gm_cat = row[7]
                cp_subcat = row[12]
                data.setdefault(country, {})
                data[country].setdefault(gm_prod, {})
                data[country][gm_prod].setdefault(gm_cat, {})
                data[country][gm_prod][gm_cat].setdefault(cp_subcat, [])
                data[country][gm_prod][gm_cat][cp_subcat].append(row)
    return data

# with open(output_file, 'a', ) as fo:
#     try:
#         writer = csv.writer(fo,
#                             delimiter=self.delimiter.decode('utf-8'),
#                             lineterminator=self.line_terminator,
#                             quotechar=self.quote_char,
#                             quoting=csv.QUOTE_ALL)
#         writer.writerows(self.failed_urls)
#         self.logger.info('Recorded non-working URLs in file: ' + output_file)
#     except csv.Error as e:
#         self.logger.error('Error in writing CSV (output) file: ' + output_file)
#         self.logger.error(str(e))
#
# self.logger.info('\n\n:::::> Total time taken: ' +
#                  str(datetime.now().replace(microsecond=0) - self.start_time) +
#                  '\n\n')

if __name__ == '__main__':
    fname = '20180330_mapping.csv'
    data = load_mappings(fname)
    for country, gm_prod in data.items():
        print("\n\nCOUNTRY=>", country, "\n==========================\n")
        for gm_prod, gm_cat in gm_prod.items():
            # print("\tGM_PRODUCT=>", gm_prod)
            if len(gm_cat.keys()) > 1:
                pdb.set_trace()
                for gm_cat, cp_subcat in gm_cat.items():
                    print("\t\tGM_CATEGORY=>", gm_cat)
                    for cp_subcat, rows in cp_subcat.items():
                        print("\t\t\tCP_SUBCATEGORY=>", cp_subcat)
                        pp.pprint(rows)
                    # pp.pprint(cp_subcat)
                import sys
                sys.exit()

    # GM_CATEGORY cannot belong to >1 CP_SUBCAT
    # GM_PRODUCT_NAME cannot belong to >1 GM_CATEGORY
    # Under each country, collect data
    # under each group of country data,
    # COUNTRY => {GM_PRODUCT_NAME_x => { GM_CATEGORY_NAME  => CP_SUBCATEGORY => row

    pdb.set_trace()
    print("finished")

