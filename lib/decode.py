from instance import *
from pyDes import des, CBC, PAD_PKCS5
from base64 import b64encode, b64decode


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
