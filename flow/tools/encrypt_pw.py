from base64 import b64encode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def encrypt_password(pw, cur_time):
    key = 'aes256-global-flow' + cur_time
    return _encrypt(pw, key)

def _encrypt(plain, key):
    iv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    plain = pad(plain.encode(), AES.block_size)
    key = key.encode()
    iv = bytes(iv)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    return b64encode(cipher.encrypt(plain))