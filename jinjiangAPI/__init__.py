import random
import time
from pyDes import des, CBC, PAD_PKCS5
from base64 import b64encode, b64decode
from instance import *
from jinjiangAPI import HttpUtil, UrlConstant


def get(url: str, params: dict = None, return_type: str = "json", app_url: bool = True):  # get request
    if app_url:
        api_url = UrlConstant.WEB_HOST + url.replace(UrlConstant.WEB_HOST, "")  # replace web host to api host
    else:
        api_url = url  # use api url
    if api_url != "":
        try:
            return HttpUtil.get_api(url=api_url, params=params, return_type=return_type)
        except Exception as err:  # if error, return None and print error
            print("get_api error: " + str(err))
    else:
        print("get_api error: url is empty")


def decrypt(string: str, token: bool = False, key: str = "KK!%G3JdCHJxpAF3%Vg9pN"):  # decrypt string
    des_cbc = des("00000000", CBC, "1ae2c94b", padmode=PAD_PKCS5)
    if token:  # token is not empty add token to key
        key = key + Vars.cfg.data.get("user_info").get("token")
    des_cbc.setKey(key)  # set key
    return des_cbc.decrypt(b64decode(string)).decode("utf-8")


def des_encrypt(string: str, token: str = None, key: str = "KK!%G3JdCHJxpAF3%Vg9pN"):  # encrypt string
    des_cbc = des("00000000", CBC, "1ae2c94b", padmode=PAD_PKCS5)
    if token is not None:  # token is not empty add token to key
        key = key + token
    des_cbc.setKey(key)  # set key
    return b64encode(des_cbc.encrypt(string)).decode("utf-8")  # encrypt and encode


class Account:  # account class for jinjiang NOVEL API
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


class Book:  # book class for jinjiang NOVEL API
    @staticmethod
    def novel_basic_info(novel_id: str) -> dict:  # get book information by novel_id
        params: dict = {"novelId": novel_id}
        return get(url="novelbasicinfo", params=params)

    @staticmethod
    def search_info(keyword: str, search_id: int = 1, page: int = 0) -> [dict, None]:  # search book by keyword
        if page == 0:
            params: dict = {"keyword": keyword, "versionCode": Vars.cfg.data['versionCode'], "type": search_id}
        else:
            if Vars.cfg.data.get("user_info").get("token") == "":
                params: dict = {
                    "keyword": keyword,
                    "type": search_id,
                    "page": page,
                    "pageSize": 20,
                    "searchType": 8,
                    "sortMode": "DESC",
                    "token": Vars.cfg.data.get("user_info").get("token"),
                    "versionCode": Vars.cfg.data['versionCode']
                }
            else:
                return print("token is empty you can't use this function")

        return get(url="associativeSearch", params=params)


class Chapter:  # chapter class for jinjiang NOVEL API
    @staticmethod
    def get_chapter_list(novel_id: str, more: int = 0, whole: int = 1) -> dict:  # get chapter list by novel_id
        params: dict = {"novelId": novel_id, "more": more, "whole": whole}
        return get(url="chapterList", params=params)

    @staticmethod
    def chapter_vip_content(novel_id: str, chapter_id: str) -> dict:
        params = {
            "novelId": novel_id,
            "chapterId": chapter_id,
            "versionCode": Vars.cfg.data['versionCode'],
            "readState": "readahead",
            "updateTime": int(time.time()),
            "token": Vars.cfg.data.get("user_info").get("token")
        }
        return get(url="chapterContent", params=params)

    @staticmethod
    def chapter_content(novel_id: str, chapter_id: str) -> dict:
        params: dict = {"novelId": novel_id, "chapterId": chapter_id}
        return get(url="chapterContent", params=params)
