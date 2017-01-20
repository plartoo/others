import os

def download_from_ftp(ftp_obj, file_to_download, dest_folder):
    if not os.path.exists(dest_folder):  # create local folder
        os.makedirs(dest_folder)

    local_file = open(os.path.join(dest_folder, file_to_download), 'wb')
    ftp_obj.retrbinary('RETR ' + file_to_download,
                       local_file.write,
                       1024)
    local_file.close()

def upload_to_ftp(ftp_obj, source_folder, file_to_upload):
    local_file = open(os.path.join(source_folder, file_to_upload), 'rb')
    ftp_obj.storbinary('STOR ' + file_to_upload, local_file)
