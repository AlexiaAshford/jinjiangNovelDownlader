import random
import time
from instance import *
from . import decode, request, UrlConstant


class Account:  # account class for jinjiang NOVEL API
    @staticmethod
    def login(username: str, password: str) -> dict:  # login and get token
        identifiers = ''.join(random.choice("0123456789") for _ in range(18)) + ":null:null"
        params = {
            "versionCode": 206,
            "loginName": username,
            "encode": 1,
            "loginPassword": decode.des_encrypt(password),
            "sign": decode.des_encrypt(identifiers),
            "brand": "Lenovo",
            "model": "Lenovo",
            "identifiers": identifiers
        }
        return request.get(url=UrlConstant.LOGIN, params=params)  # login and get token


class Chapter:  # chapter class for jinjiang NOVEL API
    @staticmethod
    def get_chapter_list(novel_id: str, more: int = 0, whole: int = 1) -> dict:  # get chapter list by novel_id
        params: dict = {"novelId": novel_id, "more": more, "whole": whole}
        return request.get(url=UrlConstant.CHAPTER_LIST, params=params)

    @staticmethod
    def chapter_vip_content(novel_id: str, chapter_id: str) -> dict:
        params = {
            "novelId": novel_id,
            "chapterId": chapter_id,
            "versionCode": Vars.cfg.data['versionCode'],
            "readState": "readahead",
            "updateTime": int(time.time()),
            "token": Vars.cfg.data.get("token")
        }
        return request.get(url=UrlConstant.CONTENT, params=params)

    @staticmethod
    def chapter_content(novel_id: str, chapter_id: str) -> dict:
        params: dict = {"novelId": novel_id, "chapterId": chapter_id}
        return request.get(url=UrlConstant.CONTENT, params=params)
