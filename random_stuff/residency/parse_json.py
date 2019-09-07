import pdb

import json
import os

im_programs = []
for i in range(1,11):
    fname = ''.join(['freida',str(i),'.txt'])
    f = os.path.join('freida_im_json', fname)
    with open(f) as json_file:
        data = json.load(json_file)
        # print(json.dumps(data['searchResults'][0], indent=4, sort_keys=True))
        for d in data['searchResults']:
            im_programs.append(
                {
                    'Accept Applications': d['pgmAcceptAppl'],
                    'Program Base Type': d['pgmBasedType'],
                    'Program Type': d['pgmType'],
                    'ERAS': d['pgmEras'],
                    'NRMP': d['pgmNrmpMatch'],
                    'Opening positions': d['pgmFirstYrPos'],
                    'Program ID': d['pgmNbr'],
                    'Program Name': d['pgmNm'],
                    'Speciality': d['specialty'],
                    'City': d['sponsorInstitutionCity'],
                    'State': d['stateNm'],
                    'Vacant Position Deadline': d['vacantPosDeadlineDt'],
                    'Vacant Position Start': d['vacantPosStartDt']
                }
            )

with open('freida_all_im_programs.txt', 'w') as outfile:
    json.dump(im_programs, outfile)

print("Combined all IM json files from Freida. Total IM program number:", len(im_programs))

