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


NOTE: Assumption made here is that we are processing the zip files in FTP location
and each of these zip files wraps ONE CSV FILE in them.

"""

import pdb
import re
import csv
from ftplib import FTP

from account_info import *
from ftp_utils import *
from my_utils import *

encoding = 'utf-16'
metafile_keyword = 'control_file_'
temp_folder = 'temp_from_ftp'

with FTP(FTP_HOST) as ftp:
    ftp.login(user = USR_OUTBOUND, passwd = PWD_OUTBOUND)
    ftp.cwd(ROOT_OUTBOUND)
    # for dir in ftp.nlst(): # TODO: uncomment this
    for dir in ['Mediatools']:  # TODO: uncomment this

        ftp.cwd('/'.join((ROOT_OUTBOUND, dir)))

        files = []
        files_with_metadata = []
        for f in ftp.nlst():
            if re.search(metafile_keyword, f, re.M|re.I):
                files_with_metadata.append(f.replace(metafile_keyword, ''))
            else:
                files.append(f)

        files_to_prepare_metadata = list(set(files) - set(files_with_metadata))

        for f in files_to_prepare_metadata:
            print("Downloading file:", f)
            download_from_ftp(ftp, f, temp_folder)
            unzip(temp_folder, f, temp_folder)
            csv_file_name = f.replace('.zip', '.csv')

            zip_file_size = get_filesize(temp_folder, f)
            unzipped_file_size = get_filesize(temp_folder, csv_file_name)
            csv_file = os.path.join(temp_folder, csv_file_name)

            print("Reading CSV file:", csv_file)
            with open(csv_file, newline='', encoding=encoding) as csv_f:
                reader = csv.reader(csv_f)
                row_count = 0
                col_count = None
                for row in reader:
                    if not col_count:
                        col_count = len(row)
                    row_count += 1

            print("zipped file size:", zip_file_size)
            print("unzipped file size:", unzipped_file_size)
            print("row count:", (row_count-1))
            print("column count:", col_count)

            metadata_file_name = csv_file_name.replace('.csv',
                                                       ''.join(['_', re.sub(r'_$','', metafile_keyword), '.csv']))
            metadata_file = os.path.join(temp_folder, metadata_file_name)
            with open(metadata_file, 'w', newline='', encoding=encoding) as csv_f:
                metadata = [
                    ['File_name', f],
                    ['Zipped_file_size', str(zip_file_size)],
                    ['Unzipped_file_size', str(unzipped_file_size)],
                    ['Row_count', str(row_count - 1)],
                    ['Column_count', str(col_count)]
                ]
                csv.writer(csv_f).writerows(metadata)

            # upload_to_ftp(ftp, temp_folder, metadata_file_name)
            exit()





print('end')
