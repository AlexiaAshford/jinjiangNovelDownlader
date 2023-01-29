import os
import re
import time

from prettytable import PrettyTable

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
def search_home_page(response: dict) -> [dict, None]:  # search book by keyword
    if response.get("code") == '200':
        return response.get("data")
    else:
        print("get book information failed, please try again.", response.get("message"))


@GET("search")
def search_book(response: dict):  # search book by keyword
    novel_info_list = []
    if response.get("items"):
        for index, novel_info in enumerate(response.get("items")):
            novel_info_list.append(template.SearchInfo(**novel_info))
    else:
        print("get book information failed, please try again.", response.get("message"))

    return novel_info_list


@GET(UrlConstant.CHAPTER_LIST)
def get_chapter_list(response):  # get chapter list by novel_id
    if response.get("message"):
        print("get chapter list failed, please try again.", response.get("message"))
        return None
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
        "token": Vars.cfg.data.get("token")
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
    def search_info(keyword: str, page: int = 0) -> [dict, None]:  # search book by keyword
        search_recommend = []
        if page == 1:
            params = {"keyword": keyword, "versionCode": Vars.cfg.data['versionCode'], "type": 1}
            for i in search_home_page(params=params):
                search_recommend.append(template.SearchInfo(
                    novelid=i.get("novelId"),
                    novelname=i.get("novelName"),
                    authorname=i.get("authorName"),
                ))
        search_result = search_book(params={
            "keyword": keyword,
            "type": 1,
            "page": page,
            "pageSize": 20,
            "searchType": 8,
            "sortMode": "DESC",
            "token": Vars.cfg.data.get("token"),
            "versionCode": Vars.cfg.data['versionCode']

        })
        if search_recommend:
            for i in search_recommend[::-1]:
                search_result.insert(0, i)

        table = PrettyTable(['序号', '书号', '书名', '作者'])
        for index, novel_info in enumerate(search_result):
            table.add_row([str(index), novel_info.novel_id, novel_info.novel_name, novel_info.author_name])
        print(table)
        print("next page:[next or n]\t previous page:[previous or p], exit:[exit or e], input index to download.")
        while True:
            input_index = input(">")
            if input_index.isdigit() and int(input_index) < len(search_result):
                break
            elif input_index == "next" or input_index == "n":
                return Book.search_info(keyword, page + 1)
            elif input_index == "previous" or input_index == "p":
                return Book.search_info(keyword, page - 1)
            elif input_index == "exit" or input_index == "e":
                return
        return search_result[int(input_index)].novel_id


__all__ = ["app", "decode", "request", "UrlConstant", 'Book']
