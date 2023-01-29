from .req import request
from .tools import get_book_id_by_url
from .decode import des_encrypt, decrypt
from functools import partial

GET = partial(request, "GET", "https://app-cdn.jjwxc.net/androidapi/")
POST = partial(request, "POST", "https://app-cdn.jjwxc.net/androidapi/")
PUT = partial(request, "PUT", "https://app-cdn.jjwxc.net/androidapi/")

__all__ = [
    "GET",
    "POST",
    "PUT",
    "get_book_id_by_url",
    "des_encrypt",
    "decrypt",
]
