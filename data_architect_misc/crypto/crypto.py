import pdb

# REF: https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet
import base64
import csv
import os
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
fn = "test_csv.csv"
feo = "test_csv_encrypted"
fdcsv = "test_csv_decrypted.csv"

with open(fn, 'r') as  fi:
    data = b''.join(l.encode(encoding) for l in fi.readlines())

token = f.encrypt(data)


with open(feo, 'wb') as fo:
    fo.write(token)

print("written encrypted data")

# f.decrypt(token)
with open(feo, 'rb') as fi:
    encrypted_data = b''.join(l for l in fi.readlines())

d_data = f.decrypt(encrypted_data).decode(encoding)

# REF: https://stackoverflow.com/a/3305964
reader = csv.reader(d_data.splitlines(), delimiter=',')
for row in reader:
    print('\t'.join(row))

print('ha')
