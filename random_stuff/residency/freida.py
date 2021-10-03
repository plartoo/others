"""
Author: Phyo Thiha
Last Modified Date: September 6, 2019
Description: Script to fetch data of residency programs.
"""

import json
from json import JSONDecodeError
import csv
import os
import sys

import requests


# URLs we need for fetching JSON pages
BASE_URL = 'https://freida.ama-assn.org'
SEARCH_PARAM_URL = 'https://freida.ama-assn.org/Freida/user/search/getProgramSearchParameters.do'
IM_URL = 'https://freida.ama-assn.org/Freida/#/programs?specialtiesToSearch=140'
FILE_NAME = '20191028_IM_FREIDA_WITH_CONTACTS.csv' # output file name

# Load program list json
PROGRAM_LIST_JSON = 'freida_all_im_programs_from_search_result.txt'#''.join(['freida_all_im_programs','.txt'])


def percentage(numerator, denominator):
    if denominator == 0:
        return 0
    else:
        return round(100 * float(numerator)/float(denominator),2)


def get_val_from_dict(dd, key_list):
    # I know this is hack-y, but this scripts is only for one-time use
    if len(key_list) == 1:
        # Sometimes, the key exists in the dict, but the value in it is None
        if (key_list[0] in dd) and (dd[key_list[0]]):
            return dd[key_list[0]]
        else:
            return 'N/A'
    elif len(key_list) == 2:
        if (key_list[0] in dd) and (dd[key_list[0]]) and \
                (key_list[1] in dd[key_list[0]]) and (dd[key_list[0]][key_list[1]]):
            return dd[key_list[0]][key_list[1]]
        else:
            return 'N/A'
    else:
        return 'Key list depth is neither 1 nor 2.'


def update_cookie_in_header(session, header, cookie_val):
    header['Cookie'] = cookie_val
    session.headers.update(header)
    return session


def main():
    with open(os.path.join('freida_im_json', PROGRAM_LIST_JSON)) as json_file:
            programs = json.load(json_file)

    header = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': '', ## we need to fill this out dynamically
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Host': 'freida.ama-assn.org',
        'Referer': 'https://freida.ama-assn.org/Freida/',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
    }

    with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='|')
        csv_writer.writerow([
            'Program ID',
            'Program Name',
            'City',
            'State',
            'Program Director',
            'Contact Info (Coordinator)',
            'Program Years',
            'Program Co-director',
            'Speciality',
            'ERAS',
            'NRMP',
            'Application Accepting This Year',
            'Application Accepting Next Year',
            'First Year Positions Open',
            'People Invited for Interview Last Year',
            'F1 Visa',
            'H1B Visa',
            'J1 Visa',
            'IMG Percent',
            'Female Percent',
            'Avg Step1 Score',
            'Min Step1 Score',
            'Min Step2 Score',
            'Offers Preliminary Positions',
            'Freida Info Last Updated',
            'Freida Survey Date',
            'Vacant Position Deadline',
            'Vacant Position Start',
            'Freida Comments',
            'Freida Custom Fields'
        ])


        with requests.Session() as session:
            session.get(IM_URL)

            # Add cookie value and update header to be similar to coming from a browser
            # *** IMPORTANT: JSESSIONID must be replaced with the one taken from a LIVE session cookie of Firefox/Chrome
            # cookie_val = session.cookies.keys()[0] + '=freida.ama-assn.org; JSESSIONID=0001UBDwa2OAlhpYrSonZ5ER9OB:3K8FUMNQ9A; optimizelyEndUserId=oeu1567731485407r0.4001470826441931; _gcl_au=1.1.2135861729.1567731486; gaMostRecentProperty=UA-77381884-1; gaMemberStatus=unknown; gaLifeStage=unknown; gaTAMID=unknown; sc.ASP.NET_SESSIONID=xqtuhzqox5jthogh0gbcwj2z; _gaLoggedInAlready=Yes; _fbp=fb.1.1567731487248.387932124; _ga=GA1.2.1875554807.1567731487; _gid=GA1.2.523068412.1567731487; __utma=7915170.1875554807.1567731487.1567731487.1567731487.1; __utmc=7915170; __utmz=7915170.1567731487.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=7915170.|4=other=unknown=1^5=Non-Member=N=1; ki_t=1567731487735%3B1567731487735%3B1567731487735%3B1%3B1; _ga_dl=https%3A//freida.ama-assn.org/freida/%23/; _ga_dt=FREIDA%20Residency%20Program%20Database%20%7C%20Medical%20Fellowship%20Database%20%7C%20AMA; _ga_cd4=none; _ga_cd7=none; _ga_cd8=none; _ga_cd21=none%2C%20none; _gaUserId=1567731488232.315681; _ga=GA1.3.1875554807.1567731487; _gid=GA1.3.523068412.1567731487; ki_s=; __utmt_corp=1; __utmb=7915170.2.9.1567731487; _gaLinkId=; _gat_gtm=1'
            cookie_val = session.cookies.keys()[0] + '=freida.ama-assn.org; optimizelyEndUserId=oeu1567731485407r0.4001470826441931; _gcl_au=1.1.2135861729.1567731486; gaMostRecentProperty=UA-77381884-1; gaMemberStatus=unknown; gaLifeStage=unknown; gaTAMID=unknown; sc.ASP.NET_SESSIONID=xqtuhzqox5jthogh0gbcwj2z; _gaLoggedInAlready=Yes; _fbp=fb.1.1567731487248.387932124; _ga=GA1.2.1875554807.1567731487; _gid=GA1.2.523068412.1567731487; __utma=7915170.1875554807.1567731487.1567731487.1567731487.1; __utmc=7915170; __utmz=7915170.1567731487.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=7915170.|4=other=unknown=1^5=Non-Member=N=1; ki_t=1567731487735%3B1567731487735%3B1567731487735%3B1%3B1; _ga_dl=https%3A//freida.ama-assn.org/freida/%23/; _ga_dt=FREIDA%20Residency%20Program%20Database%20%7C%20Medical%20Fellowship%20Database%20%7C%20AMA; _ga_cd4=none; _ga_cd7=none; _ga_cd8=none; _ga_cd21=none%2C%20none; _gaUserId=1567731488232.315681; _ga=GA1.3.1875554807.1567731487; _gid=GA1.3.523068412.1567731487; ki_s=; __utmt_corp=1; __utmb=7915170.2.9.1567731487; _gaLinkId=; _gat_gtm=1'
            session = update_cookie_in_header(session, header, cookie_val)

            # We need to make another request to get cookie that has JSESSIONID
            session.get(SEARCH_PARAM_URL)
            cookie_val = ''.join([cookie_val, '; ', session.cookies.keys()[0],'=',session.cookies.values()[0]])
            session = update_cookie_in_header(session, header, cookie_val)

            # We submit EULA agreement; only after this stage can we fetch JSONs with program detail
            session.get('https://freida.ama-assn.org/Freida/eulaSubmit.do')
            i = 0
            for prg in programs:
                program_name = prg['Program Name']
                program_detail_url = ''.join(['https://freida.ama-assn.org/Freida/user/programDetails.do?pgmNumber=',
                                              prg['Program ID']])
                pg = session.get(program_detail_url)
                print("\n", str(i), ". Fetching:", program_name)
                try:
                    detail_json = json.loads(pg.content)
                    # print(json.dumps(detail_json, indent=4, sort_keys=True))
                    # print(json.dumps(json.loads(pg.content), indent=4, sort_keys=True))
                    prg['Application Accepting This Year'] = get_val_from_dict(detail_json, ['acceptingThisYear'])
                    prg['Application Accepting Next Year'] = get_val_from_dict(detail_json, ['acceptingNextYear'])
                    prg['First Year Positions Open'] = get_val_from_dict(detail_json, ['firstYearPositions']) # May be redundant to 'Opening positions'
                    prg['People Invited for Interview Last Year'] = get_val_from_dict(detail_json, ['interviews'])
                    prg['F1 Visa'] = get_val_from_dict(detail_json, ['f1Visa'])
                    prg['H1B Visa'] = get_val_from_dict(detail_json, ['h1bVisa'])
                    prg['J1 Visa'] = get_val_from_dict(detail_json, ['j1Visa'])
                    prg['Freida Info Last Updated'] = get_val_from_dict(detail_json, ['lastUpdated'])
                    prg['Freida Survey Date'] = get_val_from_dict(detail_json, ['pgmSurveyDt'])
                    prg['Offers Preliminary Positions'] = get_val_from_dict(detail_json, ['preliminaryPositionsAvailable'])
                    prg['Freida Custom Fields'] = get_val_from_dict(detail_json, ['customFields'])
                    prg['IMG Percent'] = get_val_from_dict(detail_json, ['jsonExpandedProgram', 'xppAvgImg'])
                    prg['Female Percent'] = get_val_from_dict(detail_json, ['jsonExpandedProgram', 'xppAvgFemale'])
                    prg['Avg Step1 Score'] = get_val_from_dict(detail_json, ['jsonExpandedProgram', 'xppAvgUsmleStep1Score'])
                    prg['Min Step1 Score'] = get_val_from_dict(detail_json, ['jsonExpandedProgram', 'xppUsmleStep1Score'])
                    prg['Min Step2 Score'] = get_val_from_dict(detail_json, ['jsonExpandedProgram', 'xppUsmleStep2Score'])
                    prg['Freida Comments'] = get_val_from_dict(detail_json, ['jsonExpandedProgram', 'xppComments'])
                    prg['Program Years'] = get_val_from_dict(detail_json, ['pgmYears'])
                    prg['Codirector Info'] = get_val_from_dict(detail_json, ['programCoDirectorInfo'])
                    prg['Contact Info'] = get_val_from_dict(detail_json, ['programContactInfo'])
                    prg['Program Director Info'] = get_val_from_dict(detail_json, ['programDirectorInfo'])

                    i += 1
                    print(json.dumps(prg, indent=4, sort_keys=True))
                    csv_writer.writerow([
                        prg['Program ID'],
                        prg['Program Name'],
                        prg['City'],
                        prg['State'],
                        prg['Program Director Info'],
                        prg['Contact Info'],
                        prg['Program Years'],
                        prg['Codirector Info'],
                        prg['Speciality'],
                        prg['ERAS'],
                        prg['NRMP'],
                        prg['Application Accepting This Year'],
                        prg['Application Accepting Next Year'],
                        prg['First Year Positions Open'],
                        prg['People Invited for Interview Last Year'],
                        prg['F1 Visa'],
                        prg['H1B Visa'],
                        prg['J1 Visa'],
                        prg['IMG Percent'],
                        prg['Female Percent'],
                        prg['Avg Step1 Score'],
                        prg['Min Step1 Score'],
                        prg['Min Step2 Score'],
                        prg['Offers Preliminary Positions'],
                        prg['Freida Info Last Updated'],
                        prg['Freida Survey Date'],
                        prg['Vacant Position Deadline'],
                        prg['Vacant Position Start'],
                        prg['Freida Comments'],
                        prg['Freida Custom Fields']
                    ])
                    # Maybe we may need them later, but not now
                    # prg['Educational Benefits: International Experience'] = detail_json['internationalExperience']
                    # prg['Percentage of Full-time Female Faculty'] = detail_json['jsonExpandedProgram']['xppPctFemale']
                    # prg['Goverment Affiliated'] = detail_json['pgmGovAffilInd']
                except ValueError:
                    print("\nError parsing JSON for:", prg['Program Name'], "\tURL:", program_detail_url)
                    # sys.exit()
                except JSONDecodeError:
                    print("\nError decoding JSON for:", prg['Program Name'], "\tURL:", program_detail_url)


if __name__ == '__main__':
    main()
    print("\nFinished fetching data from Freida")
