import argparse
import datetime
import os

from crypto import Crypto
import account_info

"""
Description: Script that calls Crypto module to encrypt data.

Usage:
crypto> python encrypt.py -f C:/Users/me/Desktop/crypto/raw_files -p 123 -s C:/Users/me/Desktop/crypto/salt 
-o C:/Users/me/Desktop/crypto/2_encrypted 
"""

if __name__ == '__main__':
    datestamp = datetime.datetime.now().strftime('%Y-%m-%d')
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    raw_dir = os.path.join(cur_dir, account_info.DEFAULT_RAW_DIR)
    salt_file = os.path.join(cur_dir, account_info.DEFAULT_SALT_FILE_NAME)
    encrypted_dir = os.path.join(cur_dir, account_info.DEFAULT_ENCRYPTED_DIR)
    processed_dir = os.path.join(cur_dir, account_info.DEFAULT_PROCESSED_DIR)

    parser = argparse.ArgumentParser(description='Encrypt data file(s)')
    parser.add_argument('-f',
                        default=raw_dir,
                        type=str,
                        help='Folder path where raw file(s) to encrypt are placed.')
    parser.add_argument('-p',
                        default=account_info.PASSWORD,
                        type=str,
                        help='Password to encrypt.')
    parser.add_argument('-s',
                        default=salt_file,
                        type=str,
                        help='Salt file path+name. If you do not have salt file, '
                             'generate it by running >> python generate_salt.py')
    parser.add_argument('-o',
                        default=encrypted_dir,
                        type=str,
                        help="Folder path where encrypted/output file(s) will be placed.")
    args = parser.parse_args()

    assert os.path.exists(args.f),\
        ''.join(['Please make sure files to encrypt is placed in this folder: ', args.f])
    assert os.path.exists(args.s),\
        ''.join(['Please make sure salt file is here as: ', args.s])
    if not os.path.exists(args.o):
        print("Created output folder for encrypted files:", args.o)
        os.makedirs(args.o)
    if not os.path.exists(processed_dir):
        print("Created output folder for processed files:", processed_dir)
        os.makedirs(processed_dir)
    if not isinstance(args.p, bytes):
        args.p = args.p.encode('utf-8')

    c = Crypto()
    files = [os.path.join(args.f, f) for f in os.listdir(args.f) if os.path.isfile(os.path.join(args.f, f))]
    for f in files:
        with open(f, 'rb') as fi:
            f_name = os.path.split(f)[-1]
            name, extension = os.path.splitext(f_name)
            outfile = os.path.join(args.o, ''.join([name, '_encrypted_', datestamp, extension]))
            print("\nEncrypting:", f)
            c.encrypt_and_write(fi.read(), args.p, args.s, outfile)
        os.rename(f, os.path.join(processed_dir, f_name))
        print("Moved processed file:", os.path.join(processed_dir, f_name))
    print('\nFinished encrypting files.\n')
