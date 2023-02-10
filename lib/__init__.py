from .req import request
from .tools import GetBookid, CheckJson, CheckJsonAndAddModel
from .decode import des_encrypt, decrypt, decrypt_aes, encrypt_aes
from functools import partial
from .command import parse_args

GET = partial(request, "GET", "https://app-cdn.jjwxc.net/androidapi/")
POST = partial(request, "POST", "https://app-cdn.jjwxc.net/androidapi/")
PUT = partial(request, "PUT", "https://app-cdn.jjwxc.net/androidapi/")

__all__ = [
    "GET",
    "POST",
    "PUT",
    "parse_args",
    "GetBookid",
    "CheckJsonAndAddModel",
    "CheckJson",
    "des_encrypt",
    "decrypt",
    "decrypt_aes",
    "encrypt_aes"
]
