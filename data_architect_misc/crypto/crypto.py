import argparse
import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Crypto(object):
    CUR_DIR = os.path.dirname(os.path.realpath(__file__))
    SALT_FILE_NAME = 'salt'


    def __load_salt(self, salt_file):
        with open(salt_file, 'rb') as fi:
            return fi.read()


    @staticmethod
    def __generate_salt():
        return os.urandom(16)


    def generate_salt_file(self, dir, fname):
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


    def encrypt_and_write(self, data, password, salt_file, outfile):
        fernet = Fernet(self.generate_key(password, salt_file))
        with open(outfile, 'wb') as fo:
            fo.write(fernet.encrypt(data))
        print("Encrypted data written to:", outfile)


    def load_and_decrypt(self, encrypted_file, outfile, password, salt_file):
        fernet = Fernet(self.generate_key(password, salt_file))
        with open(encrypted_file, 'rb') as fi:
            encrypted_data = b''.join(l for l in fi.readlines())
            data = fernet.decrypt(encrypted_data)
            with open(outfile, 'wb') as fo:
                fo.write(data)
                print("Decrypted data written to:", outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='To generate salt file, use -s flag')
    parser.add_argument('-s',
                        default=0,
                        type=int,
                        help="If '1', this will generate salt file in the same directory as the code is")
    args = parser.parse_args()

    if args.s:
        c = Crypto()
        c.generate_salt_file(c.CUR_DIR, c.SALT_FILE_NAME)
