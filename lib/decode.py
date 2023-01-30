import base64
from instance import *
from Crypto.Cipher import AES
from pyDes import des, CBC, PAD_PKCS5
from base64 import b64encode, b64decode


def encrypt_aes(text, key='6jlxeTh7VgrNbB14'):
    length = 16
    count = len(text.encode('utf-8'))
    # text不是16的倍数那就补足为16的倍数
    if count % length != 0:
        add = length - (count % length)
    else:
        add = 0
    entext = text + ('\0' * add)
    aes = AES.new(str.encode(key), AES.MODE_ECB)
    enaes_text = str(base64.b64encode(aes.encrypt(str.encode(entext))), encoding='utf-8')
    return enaes_text


def decrypt_aes(data, key='6jlxeTh7VgrNbB14'):
    aes = AES.new(str.encode(key), AES.MODE_ECB)
    return str(aes.decrypt(base64.b64decode(data)), encoding='utf-8').replace('\0', '')


def pkcs7un_padding(data):
    length = len(data)
    un_padding = ord(chr(data[length - 1]))
    return data[0:length - un_padding]


def decrypt(string: str, token: bool = False, key: str = "KK!%G3JdCHJxpAF3%Vg9pN"):  # decrypt string
    des_cbc = des("00000000", CBC, "1ae2c94b", padmode=PAD_PKCS5)
    if token:  # token is not empty add token to key
        key = key + Vars.cfg.data.get("token")
    des_cbc.setKey(key)  # set key
    return des_cbc.decrypt(b64decode(string)).decode("utf-8")


def des_encrypt(string: str, token: str = None, key: str = "KK!%G3JdCHJxpAF3%Vg9pN"):  # encrypt string
    des_cbc = des("00000000", CBC, "1ae2c94b", padmode=PAD_PKCS5)
    if token is not None:  # token is not empty add token to key
        key += token
    des_cbc.setKey(key)  # set key
    return b64encode(des_cbc.encrypt(string)).decode("utf-8")  # encrypt and encode


if __name__ == '__main__':
    texts = "3rweewtewgergs是"
    # ValueError: Data must be aligned to block boundary in ECB mode,处理这个错误
    texts = texts + (16 - len(texts) % 16) * chr(16 - len(texts) % 16)  # 补位
    print('texts=\t', texts)

    print('texts=\t', encrypt_aes(texts))
    print('decrypt,key=\t', decrypt_aes(encrypt_aes(texts)))
    # print('encrypt,key=\t', encrypt_aes(texts))
    # print('decrypt,key=\t', decrypt_aes("Di6iQFdKcA8+Q+iNeORyIQ==".encode('utf-8')))
