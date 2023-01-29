import random

from .API import *
from lib import decode
from prettytable import PrettyTable


class Account:
    @staticmethod
    def login(username: str, password: str):
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
        # return request.get(url=UrlConstant.LOGIN, params=params)  # login and get token

    @staticmethod
    def user_center():
        params = {"versionCode": Vars.cfg.data['versionCode'], "token": Vars.cfg.data.get("token")}
        result = get_user_center(params=params)
        if result:
            user_info = get_user_info(params=params)
            print("用户信息:")
            print("名称:", user_info.get("nickname"))
            print("序号:", user_info.get("readerid"))
            print("等级:", user_info.get("readergrade"))
            print("余额:", result.get("balance"))
            return True


class Chapter:
    @staticmethod
    def chapter_vip_content(novel_id: str, chapter_id, cache_file_path) -> str:  # get chapter list by novel_id
        response = get_chapter_vip_content(params={
            "novelId": novel_id,
            "chapterId": chapter_id,
            "versionCode": Vars.cfg.data['versionCode'],
            "readState": "readahead",
            "updateTime": int(time.time()),
            "token": Vars.cfg.data.get("token")
        })
        if response is None:
            return "程序错误,下载失败"
        if response.get("message") is None:
            content_info = template.ContentInfo(**response)
            content_info.content = decode.decrypt(content_info.content, token=True)
            with open(cache_file_path, "w", encoding="utf-8") as f:
                f.write(content_info.chapterName + "\n")
                [f.write(i + "\n") for i in content_info.content.split("\n") if i.strip() != ""]
        else:
            return response.get("message")

    @staticmethod
    def chapter_free_content(novel_id: str, chapter_id, cache_file_path) -> str:
        response = get_chapter_free_content(params={"novelId": novel_id, "chapterId": chapter_id})
        if response is None:
            return "程序错误,下载失败"
        if response.get("message") is None:
            content_info = template.ContentInfo(**response)  # create content info
            if content_info.content:
                with open(cache_file_path, "w", encoding="utf-8") as f:
                    f.write(content_info.chapterName + "\n")
                    [f.write(i + "\n") for i in content_info.content.split("\n") if i.strip() != ""]
        else:
            return response.get("message")


class Book:
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
        # 判断是否搜索到最后一页
        if isinstance(search_result, str):
            if page == 1:
                return print(f"没有搜索到与关键词:{keyword} 相关小说")
            return print(search_result)

        table = PrettyTable(['序号', '书号', '书名', '作者'])
        for index, novel_info in enumerate(search_result):
            if len(novel_info.novel_name) > 15:
                # 七八十字的书名都有...
                novel_info.novel_name = novel_info.novel_name[:15] + "..."
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
                if page <= 1:
                    print("已经是第一页了")
                    continue
                return Book.search_info(keyword, page - 1)
            elif input_index == "exit" or input_index == "e":
                return
        return search_result[int(input_index)].novel_id


__all__ = ['Book', 'Account']
