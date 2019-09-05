"""
Author: Phyo Thiha
Last Modified Date: September 4, 2019
Description: Script to fetch data of residency programs.
"""

import csv
import re
import requests
from bs4 import BeautifulSoup

def percentage(numerator, denominator):
    return round(100 * float(numerator)/float(denominator),2)

BASE_URL = 'https://apps.acgme.org'
IM_URL = 'https://apps.acgme.org/ads/Public/Programs/Search?stateId=&specialtyId=18&specialtyCategoryTypeId=&numCode=&city='
FILE_NAME = 'IM_ACGME.csv'

with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter='|')
    # Write the header first
    csv_writer.writerow(['Speciality', 'Program Name', 'City', 'Total Approved', 'Total Filled', 'Filled Percentage',
                         'Accreditation Started', 'Accreditation Latest', 'Director First Appointed',
                         #'Coordinator Name', 'Coordinator Phone', 'Coordinator Email',
                         'Hospital URL'])

    with requests.Session() as session:
        pg = session.get(IM_URL)
        pc = BeautifulSoup(pg.content, 'html.parser')
        programs = pc.select('table#programsListView-listview.listview-table tr.listview-row')
        # Note: this is how we should prettify Beautifulsoup's tags that we captured above
        # print(BeautifulSoup(programs[0].renderContents()).prettify())

        updated_session_header = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cookie': ''.join(['BNI_persistence=',session.cookies.get('BNI_persistence')]),
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'apps.acgme.org',
            'Referer': 'https://apps.acgme.org/ads/Public/Programs/Search?stateId=&specialtyId=18&specialtyCategoryTypeId=&numCode=&city=',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
        }
        session.headers.update(updated_session_header)

        i = 0
        for prg in programs:
            specialty = prg.select('td:nth-child(3)')[0].text
            prog_name = prg.select('td:nth-child(4)')[0].text
            city = prg.select('td:nth-child(6)')[0].text

            prog_detail_url = ''.join([BASE_URL, prg.select('td:nth-child(7) > a:nth-child(1)')[0].attrs['href']])
            print("Fetching:", prog_name, "\t\t==>", prog_detail_url)
            # Now fetch the detail page
            dpg = session.get(prog_detail_url)
            dpc = BeautifulSoup(dpg.content, 'html.parser')

            total_approved_ele = dpc.find_all('dt', text=re.compile(r'Total Approved Resident'))
            total_approved = int(total_approved_ele[0].nextSibling.nextSibling.text.strip()) if total_approved_ele else -1

            total_filled_ele = dpc.find_all('dt', text=re.compile(r'Total Filled Resident'))
            total_filled = int(total_filled_ele[0].nextSibling.nextSibling.text.strip()) if total_filled_ele else 0

            total_filled_percentage = percentage(total_filled, total_approved)

            hospital_url_ele = dpc.select('#content-panel > div:nth-child(4) > a:nth-child(2)')
            hospital_url = hospital_url_ele[0].attrs['href'] if hospital_url_ele else 'N/A'

            accreditation_start_ele = dpc.find_all('dt',text=re.compile(r'Original Accreditation Date'))
            accreditation_start = accreditation_start_ele[0].nextSibling.nextSibling.text.strip() if accreditation_start_ele else 'N/A'

            accreditation_last_ele = dpc.find_all('dt',text=re.compile(r'Effective Date'))
            accreditation_last = accreditation_last_ele[0].nextSibling.nextSibling.text.strip() if accreditation_last_ele else 'N/A'

            ## Scrape them later; kind of irrelevant for now
            # coordinator_name_section = dpc.find_all('h3', text=re.compile(r'Coordinator Information'))[0].parent.parent.nextSibling.nextSibling
            # coordinator_name = coordinator_name_section.select('li:nth-child(1)')[0].text
            # coordinator_phone_section = dpc.find_all('dt', text=re.compile(r'Phone'))[1].nextSibling.nextSibling.text.strip()
            # coordinator_phone = 'x'
            # coordinator_email = 'x'

            director_first_appointed_ele = dpc.find_all('dt', text=re.compile(r'Director First Appointed'))
            director_first_appointed = director_first_appointed_ele[0].nextSibling.nextSibling.text.strip() if director_first_appointed_ele else 'N/A'
            cur_row = [specialty, prog_name, city, total_approved, total_filled, total_filled_percentage,
                       accreditation_start, accreditation_last, director_first_appointed, hospital_url]
            print(str(i), ":", cur_row, "\n")
            csv_writer.writerow(cur_row)
            i += 1
