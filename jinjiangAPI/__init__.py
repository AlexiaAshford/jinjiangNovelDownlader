import random
import time

from pyDes import des, CBC, PAD_PKCS5
from base64 import b64encode, b64decode
from instance import *
from jinjiangAPI import HttpUtil, UrlConstant


def get(url: str, params: dict = None, return_type: str = "json"):
    # if params is not None:
    #     params.update({"token": Vars.cfg.data.get("user_info").get("token")})
    try:
        api_url = UrlConstant.WEB_HOST + url.replace(UrlConstant.WEB_HOST, "")
        return HttpUtil.get_api(url=api_url, params=params, return_type=return_type)
    except Exception as err:
        print("get_api error: " + str(err))


def decrypt(string: str, token: bool = False, key: str = "KK!%G3JdCHJxpAF3%Vg9pN"):
    des_cbc = des("00000000", CBC, "1ae2c94b", padmode=PAD_PKCS5)
    if token:  # token is not empty add token to key
        key = key + Vars.cfg.data.get("user_info").get("token")
    des_cbc.setKey(key)  # set key
    return des_cbc.decrypt(b64decode(string)).decode("utf-8")


def des_encrypt(string: str, token: str = None, key: str = "KK!%G3JdCHJxpAF3%Vg9pN"):
    des_cbc = des("00000000", CBC, "1ae2c94b", padmode=PAD_PKCS5)
    if token is not None:  # token is not empty add token to key
        key = key + token
    des_cbc.setKey(key)  # set key
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
    def novel_basic_info(novel_id: str) -> dict:  # get book information by novel_id
        return get(url="novelbasicinfo", params={"novelId": novel_id})


class Chapter:
    @staticmethod
    def get_chapter_list(novel_id: str, more: int = 0, whole: int = 1) -> dict:  # get chapter list by novel_id
        return get(url="chapterList", params={"novelId": novel_id, "more": more, "whole": whole})

    @staticmethod
    def chapter_vip_content(novel_id: str, chapter_id: str) -> dict:
        params = {
            "novelId": novel_id,
            "chapterId": chapter_id,
            "versionCode": 206,
            "readState": "readahead",
            "updateTime": int(time.time()),
            "token": Vars.cfg.data.get("user_info").get("token")
        }
        return get(url="chapterContent", params=params)

    @staticmethod
    def chapter_content(novel_id: str, chapter_id: str) -> dict:
        return get(url="chapterContent", params={"novelId": novel_id, "chapterId": chapter_id})
