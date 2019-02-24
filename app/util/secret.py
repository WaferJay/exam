
import hashlib
import random

import binascii


def encrypt_password(pwd: str, salt: bytes=None):

    if salt is None:
        salt = bytearray(2)

        for i in range(2):
            salt[i] = random.randint(0, 255)

    salt_hex = binascii.b2a_hex(salt)

    pwd = pwd.encode("utf-8")
    return salt_hex.decode("ascii") + hashlib.md5(b':'.join([pwd, salt, b'Exam'])).hexdigest()[4:]


def verify_password(pwd, cipher_pwd):
    salt = binascii.a2b_hex(cipher_pwd[:4])
    pwd_c = encrypt_password(pwd, salt)
    return pwd_c == cipher_pwd

