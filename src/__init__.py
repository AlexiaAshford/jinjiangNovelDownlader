import time
import random
import database
from .API import *
import src.url_list
from instance import *
from prettytable import PrettyTable
from lib import decode, CheckJson, CheckJsonAndAddModel


class Account:
    @staticmethod
    def login(username: str, password: str):
        identifiers = ''.join(random.choice("0123456789") for _ in range(18)) + ":null:null"
        params = {
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
        @CheckJsonAndAddModel(template.UserCenter)
        @GET(url_list.getUserCenter)
        def get_user_center(response: dict):
            return response, url_list.app_host + url_list.getUserCenter

        result = get_user_center(params=None)  # type: template.UserCenter
        if result:
            @CheckJsonAndAddModel(template.UserInfo)
            @GET(url_list.getAppUserinfo)
            def get_user_info(response: dict):
                return response, url_list.app_host + url_list.getAppUserinfo

            user_info = get_user_info(params=None)  # type: template.UserInfo
            table = PrettyTable()
            table.field_names = ["名称", "序号", "等级", "余额"]
            table.add_row([user_info.nickname, user_info.readerid, user_info.readergrade, result.balance])
            print(table)
            return True


class Chapter:
    @staticmethod
    def chapter_content(novel_id: str, chapter_id, isvip):  # get chapter list by novel_id
        if isvip == 2:
            if not Vars.cfg.data.get("token"):
                return "未登录,无法下载vip章节"
            response = get_chapter_vip_content(params={
                "novelId": novel_id,
                "chapterId": chapter_id,
                "readState": "readahead",
                "updateTime": int(time.time()),
            })
        else:
            response = get_chapter_free_content(params={"novelId": novel_id, "chapterId": chapter_id})
        if response is None:
            return "程序错误,下载失败"
        if response.get("message") is None:

            return template.ContentInfo(**response)
        else:
            return response.get("message")

    @staticmethod
    def chapter_free_content(novel_id: str, chapter_id):
        response = get_chapter_free_content(params={"novelId": novel_id, "chapterId": chapter_id})
        if response is None:
            return "程序错误,下载失败"
        if response.get("message") is None:
            return template.ContentInfo(**response)
        else:
            return response.get("message")


class Book:
    @staticmethod
    def novel_basic_info(novel_id: str) -> template.BookInfo:
        @CheckJsonAndAddModel(template.BookInfo)
        @GET(url_list.novelbasicinfo)
        def novel_basic_info(response: dict):  # get book information by novel_id
            return response, url_list.app_host + url_list.novelbasicinfo

        return novel_basic_info(params={"novelId": novel_id})

    @staticmethod
    def get_chapter_list(novel_id: str):

        @CheckJson
        @GET(url_list.chapterList)
        def get_chapter_list(response):  # get chapter list by novel_id
            return response, url_list.app_host + url_list.chapterList

        download_content = []
        chapter_list = get_chapter_list(params={"novelId": novel_id, "more": 0, "whole": 1})
        if chapter_list is not None and chapter_list.get("chapterlist"):
            for chapter in chapter_list['chapterlist']:
                chap_info = template.ChapterInfo(**chapter)
                # chap_info.chaptername = re.sub(r'[\\/:*?"<>|]', '', chap_info.chaptername)

                if not database.session.query(database.ChapterSql).filter(
                        database.ChapterSql.novelId == chap_info.novelid,
                        database.ChapterSql.chapterid == chap_info.chapterid).first():
                    download_content.append(chap_info)

                database.session.add(database.CatalogueSql(
                    novelid=chap_info.novelid,
                    chapterid=chap_info.chapterid,
                    chaptername=chap_info.chaptername,
                    chaptersize=chap_info.chaptersize,
                    chapterintro=chap_info.chapterintro,
                    islock=chap_info.islock,
                    islockMessage=chap_info.islockMessage,
                    isvip=chap_info.isvip,
                    point=chap_info.point,
                    originalPrice=chap_info.originalPrice,
                    pointfreevip=chap_info.pointfreevip,
                    lastpost_time=chap_info.lastpost_time
                ))
        return download_content

    @staticmethod
    def search_info(keyword: str, page: int = 0) -> [dict, None]:  # search book by keyword
        search_recommend = []
        if page == 1:
            @GET(url_list.associativeSearch)
            def search_home_page(response: dict) -> [dict, None]:  # search book by keyword
                if response.get("code") == '200':
                    return response.get("data")
                else:
                    print("search failed:", response.get("message"))

            for i in search_home_page(params={"keyword": keyword, "type": 1}):
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
