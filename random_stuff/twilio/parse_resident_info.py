import pdb


import json

import pandas as pd


def myprint(d):
    print(json.dumps(d, indent=4))#, sort_keys=True)


def main():
    d = pd.read_excel('woodcliff_orig_20191111.xls',header=None,sheet_name=None)
    list_of_d = []
    for sheet, df in d.items():
        print('Sheet name:', sheet)
        cur_d = {}
        # pdb.set_trace()
        for index, row in df.iterrows():
            # print(row)
            if row[0] == 'General':
                if cur_d:
                    # myprint(cur_d)
                    cur_d['CountLateFee'] = sum(1 if 'Late Fee' in s else 0 for s in cur_d['CreditHistory']) if 'CreditHistory' in cur_d else 0
                    # Note: in source file, there's two variation due to spelling error for 'Late Payment Notice' and 'Late Payment Notiice'
                    cur_d['CountLateNotice'] = sum(1 if 'Late Payment' in s else 0 for s in cur_d['CreditHistory']) if 'CreditHistory' in cur_d else 0
                    cur_d['RecurringChargesStartDate'] = ''
                    cur_d['Parking'] = 0
                    cur_d['RealEstateTax'] = 0
                    cur_d['StorageFee'] = 0
                    cur_d['Mortgage'] = 0
                    cur_d['CapitalReserve'] = 0
                    cur_d['MaintenanceFee'] = 0
                    cur_d['OtherFee'] = 0

                    if 'RecurringCharges' in cur_d:
                        for s in cur_d['RecurringCharges'][1:]:
                            split_s = s.split(';')
                            if split_s[3]:
                                cur_d['RecurringChargesStartDate'] = split_s[3]
                            else:
                                cur_d['RecurringChargesStartDate'] = split_s[5] if not split_s[5] else ''

                            if split_s[1] == 'Parking/Garage' and split_s[2]:
                                cur_d['Parking'] = float(split_s[2])
                            elif split_s[1] == 'Real Estate Tax' and split_s[2]:
                                cur_d['RealEstateTax'] = float(split_s[2])
                            elif split_s[1] == 'Storage Fee' and split_s[2]:
                                cur_d['StorageFee'] = float(split_s[2])
                            elif split_s[1] == 'Mortgage' and split_s[2]:
                                cur_d['Mortgage'] = float(split_s[2])
                            elif split_s[1] == 'Capital Reserve' and split_s[2]:
                                cur_d['CapitalReserve'] = float(split_s[2])
                            elif split_s[1] == 'Maintenance Fee' and split_s[2]:
                                cur_d['MaintenanceFee'] = float(split_s[2])
                            elif split_s[1] and split_s[2]:
                                cur_d['OtherFee'] = float(split_s[2])

                    # myprint(cur_d)
                    # pdb.set_trace()
                    list_of_d.append(cur_d)

                # reset all variables and flags
                cur_d = {}
                resident_info_on_next_line = False
                recurring_charges_next_line = False
                credit_history_next_line = False

            if row[0] == 'Unit - Space - Type':
                cur_d['Unit'] = row[1].split('-')[0].strip()
                cur_d['Space'] = row[1].split('-')[1].strip()
                cur_d['Type1'] = row[1].split('-')[2].strip()
            if row[2] == 'Move In':
                cur_d['MoveInDate'] = row[3]
            if row[5] == 'Description':
                cur_d['Description'] = row[6]

            if row[0] == 'Resident - Sts - Type':
                cur_d['Resident'] = row[1].split('-')[0].strip()
                cur_d['Sts'] = row[1].split('-')[1].strip()
                cur_d['Type2'] = row[1].split('-')[2].strip()
            if row[2] == 'Move Out':
                cur_d['MoveOutDate'] = row[3]
            if row[5] == 'Accept Checks':
                cur_d['AcceptChecks'] = row[6]

            if row[0] == 'Resident Name':
                cur_d['ResidentName'] = row[1]
            if row[2] == 'Lease Beg':
                cur_d['LeaseBeginning'] = row[3]

            if row[0] == 'Co-Resident Name':
                cur_d['CoResidentName'] = row[1]
            if row[2] == 'Lease End':
                cur_d['LeaseEnding'] = row[3]

            if row[0] == 'Billing Address':
                cur_d['BillingAddress'] = row[1]
            if row[2] == 'Home Phone':
                cur_d['HomePhone'] = row[3]
            if row[5] == 'EMail':
                cur_d['Email'] = row[6]

            if row[2] == 'Work Phone':
                cur_d['WorkPhone'] = row[3]
            if row[5] == 'EMail 2':
                cur_d['Email2'] = row[6]

            if row[2] == 'Cell/Co-Cell':
                cur_d['CellPhone'] = row[3]
                cur_d['BillingAddress'] = ', '.join([str(cur_d['BillingAddress']), str(row[1])])
            if row[5] == 'Fax/Co-Fax':
                cur_d['Fax'] = row[6]

            if row[0] == 'Unit Address':
                cur_d['UnitAddress'] = row[1].strip()
            if row[5] == 'Late Charge':
                cur_d['LateCharge'] = row[6]

            if row[5] == 'NSF Check':
                cur_d['NSFCheck'] = row[6]
                cur_d['UnitAddress'] = ', '.join([str(cur_d['UnitAddress']), str(row[1])])


            if row[0] == 'Type' and row[1] == 'Name' and row[2] == 'Soc Sec':
                resident_info_on_next_line = True

            if resident_info_on_next_line and row[0] == 'ROWN':
                cur_d['ROWN'] = row[1]
                cur_d['ROWNPhone'] = row[7]
                resident_info_on_next_line = False

            if row[0] == 'Code' and row[1] == 'Description' and row[2] == 'Amount':
                recurring_charges_next_line = True
                cur_d['RecurringCharges'] = []
                # continue

            if recurring_charges_next_line and (not pd.isna(row[0])):
                cur_d['RecurringCharges'].append(';'.join(['' if pd.isna(v) else str(v) for k,v in row.iteritems()]))
            if recurring_charges_next_line and pd.isna(row[0]) and pd.isna(row[1]) and pd.isna(row[2]):
                # now we stop collecting recurring charges and will move on to credit history
                recurring_charges_next_line = False


            if row[0] == 'Code' and row[1] == 'Description' and row[2] == 'Date' and row[3] == 'Detail':
                credit_history_next_line = True
                cur_d['CreditHistory'] = []
                # continue

            if credit_history_next_line and (not pd.isna(row[0])):
                cur_d['CreditHistory'].append(';'.join(['' if pd.isna(v) else str(v) for k,v in row.iteritems()]))
            if credit_history_next_line and pd.isna(row[0]) and pd.isna(row[1]) and pd.isna(row[2]):
                # now we stop collecting recurring charges and will move on to credit history
                credit_history_next_line = False

    dff = pd.DataFrame(list_of_d, columns=['Unit', 'Space', 'Type1', 'MoveInDate',
                                           'ResidentName', 'CoResidentName', 'ROWN',
                                           'HomePhone', 'WorkPhone', 'CellPhone', 'ROWNPhone',
                                           'CountLateFee', 'CountLateNotice', 'LateCharge',
                                           'Email', 'Email2',

                                           'Parking', 'RealEstateTax', 'StorageFee', 'Mortgage', 'CapitalReserve',
                                           'MaintenanceFee', 'OtherFee',

                                           'RecurringChargesStartDate',

                                           'BillingAddress', 'UnitAddress',
                                           'LeaseBeginning', 'LeaseEnding',
                                           'Resident', 'Sts', 'Type2',
                                           'Description', 'MoveOutDate',
                                           'Fax', 'AcceptChecks', 'NSFCheck',
                                           'RecurringCharges', 'CreditHistory'
                                           ])
    dff.to_excel("woodcliff_parsed.xlsx", index=False)


if __name__ == '__main__':
    main()