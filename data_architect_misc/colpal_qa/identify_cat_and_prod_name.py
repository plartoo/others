
import pdb

import csv
import os.path
import re
import pprint
pp = pprint.PrettyPrinter(indent=4)


# # GM_CATEGORY cannot belong to >1 CP_SUBCAT
# # GM_PRODUCT_NAME cannot belong to >1 GM_CATEGORY
# # Under each country, collect data
# # under each group of country data,
# # COUNTRY => {GM_PRODUCT_NAME_x => { GM_CATEGORY_NAME  => CP_SUBCATEGORY => row
#
# def load_mappings(filename):
#     cur_dir_path = os.path.dirname(os.path.realpath(__file__))
#     url_file = os.path.join(cur_dir_path, filename)
#     data = {}
#     row_cnt = 0
#     with open(url_file, 'r') as csvfile:
#         for row in csv.reader(csvfile):
#             row_cnt +=1
#             if row_cnt == 1:
#                 header = row
#                 # print(header,"\n\n")
#             else:
#                 country = row[3]
#                 gm_prod = row[9]
#                 gm_cat = row[7]
#                 cp_subcat = row[12]
#                 data.setdefault(country, {})
#                 data[country].setdefault(gm_prod, {})
#                 data[country][gm_prod].setdefault(gm_cat, {})
#                 data[country][gm_prod][gm_cat].setdefault(cp_subcat, [])
#                 data[country][gm_prod][gm_cat][cp_subcat].append(row)
#     return (header,data)
#
#
# if __name__ == '__main__':
#     fname = '20180330_mapping.csv'
#     (header,data) = load_mappings(fname)
#     result = [header]
#     total_pairs = 0
#     for country, gm_prod in data.items():
#         i = 0
#         print(country)
#         for gm_prod, gm_cat in gm_prod.items():
#             for gm_cat, cp_subcat in gm_cat.items():
#                 if len(cp_subcat.keys()) > 1:
#                     i += 1
#                     # print("\n\n")
#                     # print("\n\n", str(i)+ ".", country, "(Country)=>", gm_prod, "(GM_PRODUCT)=>", gm_cat, "(GM_CATEGORY)")
#                     for cp_subcat, rows in cp_subcat.items():
#                         total_pairs += 1
#                         for rr in rows:
#                             result.append(rr)
#                             # print(str(i)+ ".", country, "(country)\t\t", rr[9], "(GM_Product_Name)\t\t",
#                             #       rr[7], "(GM_Category_Name)\t\t", rr[12], "(CP_Subcategory_Name)")
#
#     with open("gm_category_to_cp_subcategory_contradictions.csv", 'w') as fo:
#         writer = csv.writer(fo, delimiter=',', lineterminator='\n')
#         writer.writerows(result)
#     print("Total incidents which breaks GM_CATEGORY => CP_SUBCATEGORY rule", str(total_pairs))
#
#     result = [header]
#     total_pairs = 0
#     for country, gm_prod in data.items():
#         i = 0
#         for gm_prod, gm_cat in gm_prod.items():
#             if len(gm_cat.keys()) > 1:
#                 i += 1
#                 # print("\n\n")
#                 for gm_cat, cp_subcat in gm_cat.items():
#                     # print("\n\n", str(i)+ ".", country, "(Country)=>", gm_prod, "(GM_PRODUCT)=>", gm_cat, "(GM_CATEGORY)")
#                     for cp_subcat, rows in cp_subcat.items():
#                         total_pairs += 1
#                         for rr in rows:
#                             # print(str(i)+ ".", country, "(country)\t\t", rr[9], "(GM_Product_Name)\t\t",
#                             #       rr[7], "(GM_Category_Name)\t\t", rr[12], "(CP_Subcategory_Name)")
#                             result.append(rr)
#
#     with open("gm_product_name_to_gm_category_name_contradictions.csv", 'w') as fo:
#         writer = csv.writer(fo, delimiter=',', lineterminator='\n')
#         writer.writerows(result)
#         print("Total incidents which breaks GM_CATEGORY => CP_SUBCATEGORY rule", str(total_pairs))
#
#
#     # GM_CATEGORY cannot belong to >1 CP_SUBCAT
#     # GM_PRODUCT_NAME cannot belong to >1 GM_CATEGORY
#     # Under each country, collect data
#     # under each group of country data,
#     # COUNTRY => {GM_PRODUCT_NAME_x => { GM_CATEGORY_NAME  => CP_SUBCATEGORY => row
#     print("Finished")

# sos_product <= all where SOS_PRODUCT = 1
# sos_list_of_words = chop up GM_PRODUCT_NAME And GM_BRAND_NAME WHERE SOS_PRODUCT = 0
# sos_list_of_words = ['LOREAL', 'ELVIVE'.....]
# for w in every sos_list_of_words look for in sos_product the case WHERE w == (or is part of) GM_BRAND_NAME then print it out

def split_words(str):
    nonaphanumeric_removed = re.sub('[^0-9A-Za-z]+', ' ', str)
    return nonaphanumeric_removed.split()


def load_mappings(filename):
    cur_dir_path = os.path.dirname(os.path.realpath(__file__))
    url_file = os.path.join(cur_dir_path, filename)
    sos_prods = []
    sos_list_of_words = []

    with open(url_file, 'r') as csvfile:
        for row in csv.DictReader(csvfile):
            if row['SOS_PRODUCT'] == '1':
                sos_prods.append(row)
            else:
                sos_list_of_words += split_words(row['GM_PRODUCT_NAME'])
                sos_list_of_words += split_words(row['GM_BRAND_NAME'])
    return (sos_prods, list(set(sos_list_of_words)))


if __name__ == '__main__':
    fname = '20180411_LATAM_mappings.csv'
    (sos_prods, sos_list_of_words) = load_mappings(fname)

    with open('sos_list_of_words_used.csv', 'w') as fo:
        writer = csv.writer(fo, delimiter=',', lineterminator='\n')
        for w in sos_list_of_words:
            writer.writerow([w])

    # header = [k for k in sos_prods[0].keys()]
    # rows_with_potential_qa_issue = [header]
    # for row in sos_prods:
    #     gm_prod = set(split_words(row['GM_PRODUCT_NAME']))
    #     gm_brand = set(split_words(row['GM_BRAND_NAME']))
    #     if (not gm_prod.isdisjoint(sos_list_of_words)) or (not gm_brand.isdisjoint(sos_list_of_words)):
    #         rows_with_potential_qa_issue.append([v for v in row.values()])
    #
    # with open('20180411_prod_and_brand_name_qa.csv', 'w') as fo:
    #     writer = csv.writer(fo, delimiter=',', lineterminator='\n')
    #     writer.writerows(rows_with_potential_qa_issue)
    print('haha')