"""
Script to scan the data files in FTP location and produce metadata files
for those that don't have one already. The requirements is like this:

Data File Name:
DCM_Campaign_Report_636130080295384737_wxr45umjgmn_10252016.zip

Control File Name:
DCM_Campaign_Report_636130080295384737_wxr45umjgmn_control_file_10252016.csv

Example of columns within the control file (comma delimited):
File_name,My_test_file_name.zip
Zipped_file_size,2345
Unzipped_file_size,658564
Row_count,30
Column_count,10
"""

import pdb
import re
from ftplib import FTP

from account_info import *

metafile_keyword = 'control_file'

with FTP(FTP_HOST) as ftp:
    ftp.login(user = USR_OUTBOUND, passwd = PWD_OUTBOUND)
    ftp.cwd(ROOT_OUTBOUND)
    for dir in ftp.nlst():
        ftp.cwd('/'.join((ROOT_OUTBOUND, dir)))

        files = []
        for f in ftp.nlst():
            re.match(metafile_keyword, f, re.M|re.I)
            print(f)



print('haha')
