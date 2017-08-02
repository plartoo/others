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

import os
import re
import csv
import zipfile

from ftplib import FTP

from account_info import *
from ftp_utils import *
from my_utils import *

ENCODING = 'utf-16'
METADATA_FILE_POSTFIX = 'control_file'
TEMP_FOLDER = 'temp_from_ftp'

with FTP(FTP_HOST) as ftp:
    ftp.login(user = USR_OUTBOUND, passwd = PWD_OUTBOUND)
    ftp.cwd(ROOT_OUTBOUND)
    # for dir in ftp.nlst(): # TODO: uncomment this when we're sure we want to scan across all folders
    for dir in ['ASP', 'Celtra', 'DCM_Campaign_Report', 'DCM_Conversion_Report', 'DCM_Creative_Metadata',
                'DCM_Placement_Metadata_Report', 'Mediatools', 'NetPak', 'SpotPak', 'PrintPak', 'Vindico']:
        print("\nProcessing FTP folder:", dir)
        ftp.cwd('/'.join((ROOT_OUTBOUND, dir)))
        all_files = []
        files_with_metadata = []
        for file_from_ftp in ftp.nlst():
            if re.search(METADATA_FILE_POSTFIX, file_from_ftp, re.M|re.I):
                files_with_metadata.append(file_from_ftp.replace('_' + METADATA_FILE_POSTFIX, ''))
            else:
                all_files.append(file_from_ftp)

        files_to_prepare_metadata = list(set(all_files) - set(files_with_metadata))
        print("Files to prepare metadata are:", str(files_to_prepare_metadata))

        for source_file_name in files_to_prepare_metadata:
            print("Downloading file:", source_file_name)
            download_from_ftp(ftp, source_file_name, TEMP_FOLDER)
            files_unzipped = unzip_file(TEMP_FOLDER, source_file_name, TEMP_FOLDER)

            for file_unzipped in files_unzipped:
                zip_file_size = get_filesize(TEMP_FOLDER, source_file_name)
                unzipped_file_size = get_filesize(TEMP_FOLDER, file_unzipped)
                file_unzipped_with_path = os.path.join(TEMP_FOLDER, file_unzipped)

                print("Reading unzipped file:", file_unzipped_with_path)
                with open(file_unzipped_with_path, newline='', encoding=ENCODING) as csv_f:
                    reader = csv.reader(csv_f)
                    row_count = 0
                    col_count = None
                    for row in reader:
                        # print(row)
                        if not col_count:
                            col_count = len(row)
                        row_count += 1

                metadata_file_name = ''.join([os.path.splitext(file_unzipped)[0], '_', METADATA_FILE_POSTFIX, '.csv'])
                metadata_file_with_path = os.path.join(TEMP_FOLDER, metadata_file_name)
                print("Writing metadata file locally:", metadata_file_name)
                with open(metadata_file_with_path, 'w', newline='', encoding=ENCODING) as csv_f:
                    metadata = [
                        ['File_name', source_file_name],
                        ['Zipped_file_size', str(zip_file_size)],
                        ['Unzipped_file_size', str(unzipped_file_size)],
                        ['Row_count', str(row_count - 1)],
                        ['Column_count', str(col_count)]
                    ]
                    csv.writer(csv_f).writerows(metadata)

                print("Zipping metadata file...")
                zipped_file_name = metadata_file_name.replace('.csv', '.zip')
                zf = zipfile.ZipFile(os.path.join(TEMP_FOLDER, zipped_file_name), mode='w')
                try:
                    zf.write(metadata_file_with_path, arcname=metadata_file_name)
                finally:
                    zf.close()

                print("Uploading zipped control/metadata file to FTP...")
                upload_to_ftp(ftp, TEMP_FOLDER, zipped_file_name)

                print("Removing local temp files...")
                for f in [source_file_name, metadata_file_name, file_unzipped, zipped_file_name]:
                    file_with_path = os.path.join(TEMP_FOLDER, f)
                    os.remove(file_with_path)

print("\nCreating control/metadata files for the data export files in FTP finished successfully.")

