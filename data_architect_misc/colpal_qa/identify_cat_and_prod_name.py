
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
# REF: http://www.auladiez.com/ejercicios/16_preposiciones.php
spanish_prepositions = [
'a'
,'ante'
,'bajo'
,'cabe'
,'con'
,'contra'
,'de'
,'desde'
,'en'
,'entre'
,'hacia'
,'hasta'
,'para'
,'por'
,'según'
,'sin'
,'so'
,'sobre'
,'tras'
,'durante'
,'mediante'
,'excepto'
,'salvo'
,'incluso'
,'más'
,'menos'
,'acerca'
,'de'
,'al'
,'lado'
,'alrededor'
,'antes'
,'a pesar'
,'cerca'
,'con arreglo'
,'con objeto'
,'debajo'
,'delante'
,'dentro'
,'después'
,'detrás'
,'encima'
,'en cuanto'
,'enfrente'
,'en virtud'
,'frente'
,'fuera'
,'gracias'
,'junto'
,'lejos'
,'por'
,'culpa'
]
# REF: https://www.keepandshare.com/doc/13166/prepositions-list
english_prepositions = [
'a'
,'an'
,'the'
,'aboard'
,'about'
,'above'
,'absent'
,'according'
,'across'
,'after'
,'against'
,'ahead'
,'along'
,'alongside'
,'amid'
,'amidst'
,'among'
,'around'
,'as'
,'far'
,'well'
,'at'
,'atop'
,'before'
,'behind'
,'below'
,'beneath'
,'beside'
,'between'
,'by'
,'means'
,'of'
,'despite'
,'down'
,'due'
,'to'
,'during'
,'except'
,'far'
,'from'
,'following'
,'for'
,'in'
,'addition'
,'case'
,'front'
,'place'
,'spite'
,'inside'
,'instead'
,'in'
,'into'
,'like'
,'mid'
,'minus'
,'near'
,'next'
,'notwithstanding'
,'off'
,'on'
,'account'
,'behalf'
,'top'
]


def split_words(str):
    nonaphanumeric_removed = re.sub('[^0-9A-Za-z]+', ' ', str)
    return nonaphanumeric_removed.split()


def load_mappings(filename):
    cur_dir_path = os.path.dirname(os.path.realpath(__file__))
    url_file = os.path.join(cur_dir_path, filename)
    sos_prods = []
    sos_list_of_words = {}

    with open(url_file, 'r') as csvfile:
        for row in csv.DictReader(csvfile):
            if row['SOS_PRODUCT'] == '1':
                sos_prods.append(row)
            else:
                sos_list_of_words.setdefault(row['GM_COUNTRY_NAME'], set())
                for w in (split_words(row['GM_PRODUCT_NAME']) + split_words(row['GM_BRAND_NAME'])):
                    if not ignore_this_word(w):
                        sos_list_of_words[row['GM_COUNTRY_NAME']].add(w)
    return (sos_prods, sos_list_of_words)

def ignore_this_word(w):
    if len(w) < 3:
        return True
    elif re.match(r'^\d+$', w, re.I): # words with all numerical letters in it
        return True
    elif w in set(spanish_prepositions+english_prepositions):
        return True
    else:
        return False

if __name__ == '__main__':
    fname = '20180411_LATAM_mappings.csv'
    (sos_prods, sos_list_of_words) = load_mappings(fname)

    # # print out words that we use to check against brand and product names for reviewing
    # with open('20180411_2_sos_list_of_words_used.csv', 'w') as fo:
    #     writer = csv.writer(fo, delimiter=',', lineterminator='\n')
    #     for k,v in sos_list_of_words.items():
    #         for w in v:
    #             writer.writerow([k,w])

    header = [k for k in sos_prods[0].keys()]
    rows_with_potential_qa_issue = [header]
    for row in sos_prods:
        gm_prod = set(split_words(row['GM_PRODUCT_NAME']))
        gm_brand = set(split_words(row['GM_BRAND_NAME']))
        if (not gm_prod.isdisjoint(sos_list_of_words[row['GM_COUNTRY_NAME']])) \
                or (not gm_brand.isdisjoint(sos_list_of_words[row['GM_COUNTRY_NAME']])):
            rows_with_potential_qa_issue.append([v for v in row.values()])

    with open('20180411_prod_and_brand_name_qa.csv', 'w') as fo:
        writer = csv.writer(fo, delimiter=',', lineterminator='\n')
        writer.writerows(rows_with_potential_qa_issue)
    print('haha')