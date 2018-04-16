import argparse
import datetime
import os

from crypto import Crypto
import account_info

"""
Description: Script that calls Crypto module to decrypt data.

Usage:
crypto> python decrypt.py -f C:/Users/me/Desktop/crypto/raw_files -p 123 -s C:/Users/me/Desktop/crypto/salt 
-o C:/Users/me/Desktop/crypto/3_decrypted 
"""

if __name__ == '__main__':
    datestamp = datetime.datetime.now().strftime('%Y-%m-%d')
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    raw_dir = os.path.join(cur_dir, account_info.DEFAULT_RAW_DIR)
    salt_file = os.path.join(cur_dir, account_info.DEFAULT_SALT_FILE_NAME)
    encrypted_dir = os.path.join(cur_dir, account_info.DEFAULT_ENCRYPTED_DIR)
    processed_dir = os.path.join(cur_dir, account_info.DEFAULT_PROCESSED_DIR)
    decrypted_dir = os.path.join(cur_dir, account_info.DEFAULT_DECRYPTED_DIR)

    parser = argparse.ArgumentParser(description='Decrypt data file(s)')
    parser.add_argument('-f',
                        default=encrypted_dir,
                        type=str,
                        help='Folder path where file(s) to decrypt are placed.')
    parser.add_argument('-p',
                        default=account_info.PASSWORD,
                        type=str,
                        help='Password to decrypt.')
    parser.add_argument('-s',
                        default=salt_file,
                        type=str,
                        help='Salt file path+name. If you do not have salt file, '
                             'ask the encryptor for it.')
    parser.add_argument('-o',
                        default=decrypted_dir,
                        type=str,
                        help="Folder path where decrypted/output file(s) will be placed.")
    args = parser.parse_args()

    assert os.path.exists(args.f),\
        ''.join(['Please make sure files to decrypt is placed in this folder: ', args.f])
    assert os.path.exists(args.s),\
        ''.join(['Please make sure the salt file is here as: ', args.s])
    if not os.path.exists(args.o):
        print("Created output folder for decrypted files:", args.o)
        os.makedirs(args.o)
    if not os.path.exists(processed_dir):
        print("Created output folder for processed files:", processed_dir)
        os.makedirs(processed_dir)
    if not isinstance(args.p, bytes):
        args.p = args.p.encode('utf-8')

    c = Crypto()
    files = [os.path.join(args.f, f) for f in os.listdir(args.f) if os.path.isfile(os.path.join(args.f, f))]
    for f in files:
        f_name = os.path.split(f)[-1]
        name, extension = os.path.splitext(f_name)
        outfile = os.path.join(args.o, ''.join([name, '_decrypted_', datestamp, extension]))
        c.load_and_decrypt(f, outfile, args.p, args.s)
        os.rename(f, os.path.join(processed_dir, f_name))
        print("Moved processed file:", os.path.join(processed_dir, f_name))
    print('\nFinished decrypting files.\n')
