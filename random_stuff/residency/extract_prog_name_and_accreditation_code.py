# A quick script to extract applied programs from ERAS HTML files.

import re

import pandas as pd


IN_FILE_NAMES = ['ERAS_Programs_Applied_1.html', 'ERAS_Programs_Applied_2.html', 'ERAS_Programs_Applied_3.html']
OUT_FILE_NAME = 'Extracted_Accreditation_ID.xlsx'
accreditation_ids = []
for in_file in IN_FILE_NAMES:
    with open(in_file) as f:
        i = 0
        for line in f.readlines():
            i += 1
            print(f"{i}. {line}")

            if re.search(r'div _ngcontent-rjn.*?left;">\s\d+', line):
                accreditation_ids.append(re.findall(r'div _ngcontent-rjn.*?left;">\s(\d+)', line)[0])

df = pd.DataFrame(accreditation_ids, columns=['Accreditation_IDs'])
df.to_excel(OUT_FILE_NAME, index=False)
