import random

from pyDes import des, CBC, PAD_PKCS5
from base64 import b64encode, b64decode

from jinjiangAPI import HttpUtil, UrlConstant


def get(url: str, params: dict = None, return_type: str = "json"):
    try:
        api_url = UrlConstant.WEB_HOST + url.replace(UrlConstant.WEB_HOST, "")
        return HttpUtil.get_api(url=api_url, params=params, return_type=return_type)
    except Exception as err:
        print("get_api error: " + str(err))


def decrypt(string: str, token: str = None, key: str = "KK!%G3JdCHJxpAF3%Vg9pN"):
    des_cbc = des("00000000", CBC, "1ae2c94b", padmode=PAD_PKCS5)
    if token is not None:  # token is not empty add token to key
        key_with_token = key + token
    else:
        key_with_token = key
    des_cbc.setKey(key_with_token)  # set key
    return des_cbc.decrypt(b64decode(string)).decode("utf-8")


def des_encrypt(string: str, token: str = None, key: str = "KK!%G3JdCHJxpAF3%Vg9pN"):
    des_cbc = des("00000000", CBC, "1ae2c94b", padmode=PAD_PKCS5)
    if token is not None:  # token is not empty add token to key
        key_with_token = key + token
    else:
        key_with_token = key
    des_cbc.setKey(key_with_token)  # set key
    return b64encode(des_cbc.encrypt(string)).decode("utf-8")  # encrypt and encode


class Account:
    @staticmethod
    def login(username: str, password: str) -> dict:  # login and get token
        identifiers = ''.join(random.choice("0123456789") for _ in range(18)) + ":null:null"
        params = {
            "versionCode": 206,
            "loginName": username,
            "encode": 1,
            "loginPassword": des_encrypt(password),
            "sign": des_encrypt(identifiers),
            "brand": "Lenovo",
            "model": "Lenovo",
            "identifiers": identifiers
        }
        return get(url="login", params=params)  # login and get token


class Book:
    @staticmethod
    def book_information(novel_id: str) -> dict:  # get book information by novel_id
        return get(url="novelbasicinfo", params={"novelId": novel_id})


class Chapter:
    @staticmethod
    def chapter_information(novel_id: str, more: int = 0, whole: int = 1) -> dict:
        return get(url="chapterList", params={"novelId": novel_id, "more": more, "whole": whole})

    @staticmethod
    def chapter_content(novel_id: str, chapter_id: str, vip_chapter: bool = False) -> dict:
        if vip_chapter:
            params = {"novelId": novel_id, "chapterId": chapter_id, "versionCode": 206, "readState": "readahead"}
        else:
            params = {"novelId": novel_id, "chapterId": chapter_id}
        return get(url="chapterContent", params=params)
