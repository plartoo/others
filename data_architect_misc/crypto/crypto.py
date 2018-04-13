import base64
import csv
import io
import os
import sys

import pandas as pd
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Crypto(object):
    ENCODING = 'utf-8'
    CUR_DIR = os.path.dirname(os.path.realpath(__file__))
    ENCRYPTED_FILE_NAME = 'encrypted_data'
    SALT_FILE_NAME = 'salt'
    ENCRYPTED_FILE = os.path.join(CUR_DIR, ENCRYPTED_FILE_NAME)
    SALT_FILE = os.path.join(CUR_DIR, SALT_FILE_NAME)


    def __load_salt(self, salt_file=SALT_FILE):
        with open(salt_file, 'rb') as fi:
            return fi.read()


    @staticmethod
    def __generate_salt():
        return os.urandom(16)


    def generate_salt_file(self, dir=CUR_DIR, fname=SALT_FILE_NAME):
        salt_file = os.path.join(dir, fname)
        with open(salt_file, 'wb') as fo:
            fo.write(self.__generate_salt())
        print("New salt file generated at:", salt_file)


    def generate_key(self, password, salt_file=None):
        # REF: https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet
        if not salt_file:
            self.generate_salt_file()
            salt = self.__load_salt()
        else:
            salt = self.__load_salt(salt_file)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password))


    def encrypt_and_write(self, data, password, salt_file=SALT_FILE, outfile=ENCRYPTED_FILE):
        fernet = Fernet(self.generate_key(password, salt_file))
        with open(outfile, 'wb') as fo:
            fo.write(fernet.encrypt(data))
        print("Encrypted data written to:", outfile)


    def load_and_decrypt(self, encrypted_file, outfile, password, salt_file=SALT_FILE):
        fernet = Fernet(self.generate_key(password, salt_file))
        with open(encrypted_file, 'rb') as fi:
            encrypted_data = b''.join(l for l in fi.readlines())
            data = fernet.decrypt(encrypted_data).decode(self.ENCODING)
            with open(outfile, 'w') as fo:
                fo.write(data)


if __name__ == '__main__':
    c = Crypto()
    with open(os.path.join('temp','temp_test_xlsx.csv'), 'r') as fi:
        data = b''.join(l.encode(c.ENCODING) for l in fi.readlines())
        c.encrypt_and_write(data, b'123')
    # c.generate_salt_file()
    print("Done")

# https://stackoverflow.com/questions/9884353/xls-to-csv-converter
# https://gist.github.com/scottming/99c09685360376d4cac2de7c891e8050/9670acd5044d11871188e04b8123263ad132f512