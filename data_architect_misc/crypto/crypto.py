import pdb

# REF: https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet
import base64
import csv
import os
import sys

import pandas as pd
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
password = b'pwd'
salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))
f = Fernet(key)

encoding = 'utf-8'
# fn = "test_csv.csv"
# feo = "test_csv_encrypted"
# fdcsv = "test_csv_decrypted.csv"

fn = "test_xls.xls"
fn_temp = "temp_" + fn
feo = "test_xls_encrypted"
fdcsv = "test_xls_decrypted.csv"
dir_path = os.path.dirname(os.path.realpath(__file__))
temp_path = os.path.join(dir_path, 'temp')

if os.path.splitext(fn)[-1] in ['.xlsx', '.xls']:
    # TODO: https://stackoverflow.com/a/48435144
    pd.read_excel(fn).to_csv(os.path.join(temp_path, fn_temp), index=False)
    with open(fn_temp, 'r') as  fi:
        data = b''.join(l.encode(encoding) for l in fi.readlines())
elif os.path.splitext(fn)[-1] in ['.csv']:
    with open(fn, 'r') as  fi:
        data = b''.join(l.encode(encoding) for l in fi.readlines())
else:
    sys.exit('The file is neither Excel or CSV. This program only encrypts aformentioned file types...')

token = f.encrypt(data)

with open(feo, 'wb') as fo:
    fo.write(token)

with open(feo, 'rb') as fi:
    encrypted_data = b''.join(l for l in fi.readlines())

d_data = f.decrypt(encrypted_data).decode(encoding)

# REF: https://stackoverflow.com/a/3305964
d_data_to_write = []
reader = csv.reader(d_data.splitlines(), delimiter=',')
for row in reader:
    d_data_to_write.append((row))
    # print('\t'.join(row))

with open(fdcsv, 'w', newline='', encoding=encoding) as fo:
    writer = csv.writer(fo)
    writer.writerows(d_data_to_write)

print('ha')


# Other refs:
# https://www.blog.pythonlibrary.org/2016/05/18/python-3-an-intro-to-encryption/
# https://stackoverflow.com/a/39356747

