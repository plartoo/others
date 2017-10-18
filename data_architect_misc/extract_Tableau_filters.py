"""
Author: Phyo Thiha
Description:
Example of how to extract user filters from Tableau workbook files (TWB).
Ref: https://pastebin.com/bruVTSmN
"""
from xml.etree import ElementTree
import re
import pprint

twbFileName = './Prisma Compliance Dashboards.twb'

with open(twbFileName, 'rt') as f:
    tree = ElementTree.parse(f)
    root = tree.getroot()
    blocks = ['[User Filter 1]', '[User Filter - Agency]', '[User Filter 2]']
    filter_name = ['[COUNTRY]', '[AgencyName]', '[MasterClientName]']
    filter_summary = {}
    for i,b in enumerate(blocks):
        for gp in root.findall(".//groupfilter/..[@name='{}']//groupfilter[@function='filter']".format(b)):
            if ('expression' in gp.attrib) and (re.search(r'^ISCURRENTUSER.*', gp.attrib['expression'], re.M|re.I)):
                user = re.search(r'\.net\\(.*)\'\)', gp.attrib['expression'], re.M|re.I).group(1)
                if user not in filter_summary:
                    filter_summary[user] = {}
                for child in gp.iter('groupfilter'):
                    if filter_name[i] not in filter_summary[user]:
                        filter_summary[user][filter_name[i]] = []

                    if ('member' in child.attrib) and (child.attrib['member'] != '%null%'):
                        # print(user, ':',filter_name[i], ':::', child.attrib['member'])
                        filter_summary[user][filter_name[i]].append(child.attrib['member'])
                    elif ('to' in child.attrib) and (child.attrib['to'] != '%null%'):
                        # print(user, ':',filter_name[i], ':::', child.attrib['to'])
                        filter_summary[user][filter_name[i]].append(child.attrib['to'])

    pprint.pprint(filter_summary)

