"""
Author: Phyo Thiha
Last Modified Date: September 5, 2019
Description: Script to extract header/section labels so that
we can determine the type of information shared on this site.
"""

import csv
import requests
from bs4 import BeautifulSoup


BASE_URL = 'https://apps.acgme.org'
IM_URL = 'https://apps.acgme.org/ads/Public/Programs/Search?stateId=&specialtyId=18&specialtyCategoryTypeId=&numCode=&city='
FILE_NAME = 'IM_ACGME_Fields.csv'

with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter='|')

    info_labels = {}
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
            prog_name = prg.select('td:nth-child(4)')[0].text
            prog_detail_url = ''.join([BASE_URL, prg.select('td:nth-child(7) > a:nth-child(1)')[0].attrs['href']])
            print(str(i), ". Fetching:", prog_name, "\t\t==>", prog_detail_url)
            # Now fetch the detail page
            dpg = session.get(prog_detail_url)
            dpc = BeautifulSoup(dpg.content, 'html.parser')

            # 'dt' usually wraps header/section labels
            pg_fields = dpc.find_all('dt')
            for f in pg_fields:
                if not f.text in info_labels:
                    info_labels[f.text] = 'Found'
            i += 1
            csv_writer.writerow([prog_name, prog_detail_url] + list(info_labels.keys()))
