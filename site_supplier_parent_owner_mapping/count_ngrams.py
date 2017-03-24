"""
This script splits string values in each of the specified columns
into n-grams (where 'n' is  defined by the user) and counts their
occurrence. The count table for each n-gram is written back out as
CSV files.

This is used to inspect the most commonly occuring groups of words
in the mapping files that we have to do for Benchmarking report.

Author: Phyo Thiha
Last Modified Date: March 24, 2017
"""

import csv
from nltk import ngrams

input_file = 'mappings_utf16.csv'
grams = list(range(2,6)) # create bi-, tri-, quad-, pent-gram
ngram_tables = [{} for i in grams]

with open(input_file, encoding='utf-16') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')

    for row in csv_reader:
        site = row[1].lower()
        supplier = row[2].lower()
        parent_owner = row[3].lower()
        updated_site = row[4].lower()
        updated_supplier = row[5].lower()

        for s in [site, supplier, parent_owner, updated_site, updated_supplier]:
            for i, n in enumerate(grams):
                tokens = list(ngrams(list(s), n))

                for t in tokens:
                    cur_gram = ''.join(t)
                    if cur_gram in ngram_tables[i]:
                        ngram_tables[i][cur_gram] += 1
                    else:
                        ngram_tables[i][cur_gram] = 1

for i, t in enumerate(ngram_tables):
    with open(''.join([str(grams[i]),'.csv']), 'w', newline='', encoding='utf-16') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='\t')
        csv_writer.writerows(t.items())

def find_ngrams(input_list, n): # this is my homebrew ngram generator; for now, we'll just use the one from nltk
  return zip(*[input_list[i:] for i in range(n)])

