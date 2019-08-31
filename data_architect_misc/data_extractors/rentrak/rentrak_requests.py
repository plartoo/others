"""
Author: Phyo Thiha
Last Modified Date: August 29, 2019
Description: This is a script that demos how we can scrape data tables within
RenTrak's website. Since the website only shows up to two-digit decimal
accuracy, we will not use this script for production. Instead, we will
use Selenium to download the Excel file, which has up to four-digit
decimal accuracy.
"""

import account_info
import re

# http://docs.python-requests.org/en/master/user/quickstart/
import requests

# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# alternatively for parsing, we can try this: http://lxml.de/index.html#introduction
from bs4 import BeautifulSoup

BASE_URL = 'https://national-tv.rentrak.com'
LOGIN_URL = 'https://national-tv.rentrak.com/login.html'

# Note: PAYLOAD is stored in account_info for security reason.
# But it should look like below
# PAYLOAD = {
#     'login_id':	'', # enter username here
#     'password':	'', # enter pwd here
#     'login': 'LOGIN',
#     'url': ''
# }

# REF: use sessoins https://stackoverflow.com/a/17633072/1330974
with requests.Session() as session:
    # Step 1. Log into the website
    pg = session.post(LOGIN_URL, data=account_info.PAYLOAD)
    pc = BeautifulSoup(pg.content, 'html.parser') # parsed contents
    tags_under_bookmark = pc(text=re.compile(r'Manage Bookmarks'))[0].parent.parent
    tags_with_report_urls = tags_under_bookmark.find_all('a', href=re.compile(r'reports'))

    # Step 2. Fetch reports that we created/bookmarked
    report_url = ''.join([BASE_URL, tags_with_report_urls[0].get('href')])
    print("Fetching report: ", report_url)
    report_pg = session.get(report_url)
    report_html = BeautifulSoup(report_pg.content, 'html.parser')

    # Step 3. Prepare HTML report name that will be used to save the output from fetching.
    report_name = tags_with_report_urls[0].text
    report_name = report_html.find_all('span', id='savedBookmarkName')[0].text
    # turn the name into all lowercase with underscores.
    report_file_name = ''.join([re.sub(r'[\W]+','_', report_name).lower(),'_view_all.html'])

    # Step 4. Fetch 'ALL' page in the bookmarked report to get all data in the table
    paging_section = report_html.find_all('div', id='paging-top')[0]
    view_all_button = paging_section.find_all('a', text=re.compile(r'All', re.I))[0]
    view_all_url = ''.join([BASE_URL, view_all_button.get('href')])
    print("Downloading view all page:", view_all_url)
    excel_report = session.get(view_all_url)

    # Step 5. Save the resulting HTML so that we can parse it with, say, Pandas later
    with open(report_file_name, 'wb') as f:
        f.write(excel_report.content)

    print('Done fetching data pages.')

    # Note: tried downloading the Excel download link, but got HTML report instead.
    # report_file_name = ''.join([re.sub(r'[\W]+','_', report_name).lower(),'.xlsx'])
    # excel_download_button = report_html.find_all('a',text=re.compile(r'Excel', re.I))[0] # Or we can also use report_html.find_all('a',title='Download Report to Excel')
    # excel_download_url = ''.join([BASE_URL, excel_download_button.get('href')])
    # print("Downloading Excel report: ", excel_download_url)
    # excel_report = session.get(report_url)
    # with open(report_file_name, 'wb') as f:
    #     f.write(excel_report.content)

###
# Note: These are notes during the development of this script for my own future reference.
# Please ignore.
#
#
# first, try to download data using 'Excel' link and show that it is possible.
# then, try to automatically create links for download using this approach below:
# E.g., for AMC:::
#https://national-tv.rentrak.com/reports/market_month_trend.export?comp_format=excel;dsr_hideshow_hh_rating=hh_rating;dsr_sort_MarketMonthlyTrends=market_name%20broadcast_month;
#network_no=401;
#page_cache_id=IKEhQlOJ5eOptuJhxqp7XQ_22106300;
#simple_month_range=20160101%2000%3A00%3A00;
#simple_month_range=20171201%2000%3A00%3A00;
#tv_market_no=662;tv_market_no=525;tv_market_no=532;tv_market_no=790;tv_market_no=644;tv_market_no=583;tv_market_no=634;tv_market_no=743
#
# In the above URL, network_no is from
# ul#network_no_list.treeFilter li.header.depth-0 ul.searchable-tree li.last.nonselectable.open.depth-1 ul li.open.depth-2 ul li.leaf.depth-3
#
# page_cache_id is from
#    </head>
#    <body class="site-news-update tve" onload="callInitFuncs();"
#        data-page-cache-id="4hUEOSxBuG9nPUlOwUsBA_22106240"
#        data-use-ecache=""
#        data-page-request-no="26253984"
#        data-is-frontend-api-enabled="1"
#    >
#
# simple_month_range is from
# select#simple_month_range_from_select
# and
# select#simple_month_range_to_select
#
#tv_market_no can be fetched from here
#  ul#tv_market_no_list.treeFilter li.header.nonselectable.depth-0 ul.searchable-tree li.last.open.depth-1 ul li.leaf.depth-2
# or from here:
# ul#tv_market_no_list.treeFilter li.leaf depth-3 span.v

# for 'ALL' view, the URL becomes like below (with no_paging=1 and use_ecache=sortpage added)
#/reports/market_month_trend.html?
#dsr_hideshow_hh_rating=hh_rating;dsr_sort_MarketMonthlyTrends=market_name%20broadcast_month;
#network_no=401;
#no_paging=1;
#;use_ecache=sortpage
#page_cache_id=0R4PyOKq9q5kxNbJYQTyQ_22109096;simple_month_range=20160101%2000%3A00%3A00;
#simple_month_range=20171201%2000%3A00%3A00;tv_market_no=662;tv_market_no=525;tv_market_no=532;tv_market_no=790;tv_market_no=644;tv_market_no=583;tv_market_no=634;tv_market_no=743;tv_market_no=524;tv_market_no=520;tv_market_no=635;tv_market_no=800;tv_market_no=512;tv_market_no=537;tv_market_no=716;tv_market_no=692;tv_market_no=821;tv_market_no=756;tv_market_no=746;tv_market_no=502;tv_market_no=630;tv_market_no=559;tv_market_no=757;tv_market_no=506;tv_market_no=736;tv_market_no=514;tv_market_no=523;tv_market_no=754;tv_market_no=767;tv_market_no=637;tv_market_no=648;tv_market_no=564;tv_market_no=519;tv_market_no=517;tv_market_no=584;tv_market_no=575;tv_market_no=759;tv_market_no=602;tv_market_no=868;tv_market_no=515;tv_market_no=598;tv_market_no=510;tv_market_no=752;tv_market_no=604;tv_market_no=546;tv_market_no=522;tv_market_no=535;tv_market_no=673;tv_market_no=600;tv_market_no=623;tv_market_no=682;tv_market_no=542;tv_market_no=751;tv_market_no=679;tv_market_no=505;tv_market_no=606;tv_market_no=676;tv_market_no=565;tv_market_no=765;tv_market_no=516;tv_market_no=801;tv_market_no=802;tv_market_no=649;tv_market_no=745;tv_market_no=724;tv_market_no=513;tv_market_no=866;tv_market_no=571;tv_market_no=670;tv_market_no=509;tv_market_no=592;tv_market_no=798;tv_market_no=773;tv_market_no=563;tv_market_no=755;tv_market_no=658;tv_market_no=518;tv_market_no=545;tv_market_no=567;tv_market_no=647;tv_market_no=636;tv_market_no=566;tv_market_no=569;tv_market_no=533;tv_market_no=710;tv_market_no=766;tv_market_no=744;tv_market_no=618;tv_market_no=691;tv_market_no=758;tv_market_no=527;tv_market_no=718;tv_market_no=639;tv_market_no=561;tv_market_no=574;tv_market_no=734;tv_market_no=603;tv_market_no=747;tv_market_no=616;tv_market_no=557;tv_market_no=702;tv_market_no=582;tv_market_no=642;tv_market_no=643;tv_market_no=551;tv_market_no=749;tv_market_no=839;tv_market_no=541;tv_market_no=558;tv_market_no=722;tv_market_no=693;tv_market_no=803;tv_market_no=529;tv_market_no=651;tv_market_no=503;tv_market_no=669;tv_market_no=737;tv_market_no=553;tv_market_no=813;tv_market_no=640;tv_market_no=711;tv_market_no=528;tv_market_no=617;tv_market_no=613;tv_market_no=687;tv_market_no=762;tv_market_no=686;tv_market_no=628;tv_market_no=828;tv_market_no=698;tv_market_no=570;tv_market_no=659;tv_market_no=622;tv_market_no=501;tv_market_no=544;tv_market_no=740;tv_market_no=633;tv_market_no=650;tv_market_no=652;tv_market_no=534;tv_market_no=631;tv_market_no=632;tv_market_no=804;tv_market_no=656;tv_market_no=597;tv_market_no=675;tv_market_no=504;tv_market_no=753;tv_market_no=508;tv_market_no=500;tv_market_no=820;tv_market_no=552;tv_market_no=521;tv_market_no=717;tv_market_no=560;tv_market_no=764;tv_market_no=811;tv_market_no=556;tv_market_no=573;tv_market_no=538;tv_market_no=611;tv_market_no=610;tv_market_no=862;tv_market_no=576;tv_market_no=770;tv_market_no=661;tv_market_no=641;tv_market_no=825;tv_market_no=807;tv_market_no=855;tv_market_no=507;tv_market_no=819;tv_market_no=657;tv_market_no=612;tv_market_no=624;tv_market_no=725;tv_market_no=588;tv_market_no=881;tv_market_no=543;tv_market_no=619;tv_market_no=638;tv_market_no=609;tv_market_no=555;tv_market_no=530;tv_market_no=539;tv_market_no=581;tv_market_no=547;tv_market_no=605;tv_market_no=540;tv_market_no=531;tv_market_no=789;tv_market_no=671;tv_market_no=760;tv_market_no=709;tv_market_no=526;tv_market_no=626;tv_market_no=625;tv_market_no=511;tv_market_no=549;tv_market_no=705;tv_market_no=548;tv_market_no=554;tv_market_no=627;tv_market_no=678;tv_market_no=577;tv_market_no=550;tv_market_no=810;tv_market_no=536;tv_market_no=771;tv_market_no=596

