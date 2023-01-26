import os
import re
import time
import template
from . import *
from lib import GET, POST
from tqdm import tqdm
from . import UrlConstant
from instance import Vars


@GET(UrlConstant.NOVEL_INFO)
def novel_basic_info(response: dict) -> template.BookInfo:  # get book information by novel_id
    if response.get("message") is None:  # get book information success then print book information.
        return template.BookInfo(**response)  # create book object from book information.
        # print book information with book detail.
    else:
        print("get book information failed, please try again.", response.get("message"))


@GET(UrlConstant.SEARCH_INFO)
def search_book(response: dict) -> [dict, None]:  # search book by keyword
    if response.get("message") is None:  # get book information success then print book information.
        return response  # create book object from book information.
        # print book information with book detail.
    else:
        print("get book information failed, please try again.", response.get("message"))


@GET(UrlConstant.CHAPTER_LIST)
def get_chapter_list(response):  # get chapter list by novel_id
    download_content = []
    for chapter in tqdm(response['chapterlist'], ncols=100):
        chap_info = template.ChapterInfo(**chapter)
        chap_info.chaptername = re.sub(r'[\\/:*?"<>|]', '', chap_info.chaptername)
        chap_info.cache_file_path = os.path.join(Vars.current_command.cache,
                                                 chap_info.novelid + "-" +
                                                 chap_info.chapterid + "-" +
                                                 chap_info.chaptername + ".txt"
                                                 )
        if os.path.exists(chap_info.cache_file_path):
            pass
            # print(chap_info.chaptername, "is exists, skip it")
        else:
            if chap_info.originalPrice == 0:
                download_content.append(chap_info)
    return download_content


@GET(UrlConstant.CONTENT)
def chapter_vip_content(novel_id: str, chapter_id: str) -> dict:
    params = {
        "novelId": novel_id,
        "chapterId": chapter_id,
        "versionCode": Vars.cfg.data['versionCode'],
        "readState": "readahead",
        "updateTime": int(time.time()),
        "token": Vars.cfg.data.get("user_info").get("token")
    }
    return request.get(url=UrlConstant.CONTENT, params=params)


@GET(UrlConstant.CONTENT)
def chapter_content(novel_id: str, chapter_id: str) -> dict:
    params: dict = {"novelId": novel_id, "chapterId": chapter_id}
    return request.get(url=UrlConstant.CONTENT, params=params)


class Book:  # book class for jinjiang NOVEL API
    @staticmethod
    def novel_basic_info(novel_id: str) -> template.BookInfo:
        return novel_basic_info(params={"novelId": novel_id})

    @staticmethod
    def get_chapter_list(novel_id: str) -> dict:
        return get_chapter_list(params={"novelId": novel_id, "more": 0, "whole": 1})

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
                return print("next page is not supported yet,you need to use the first page")
        return search_book(params=params)


__all__ = ["app", "decode", "request", "UrlConstant", 'Book']
