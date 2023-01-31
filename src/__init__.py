import random
import time
import database
from instance import *
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
                "versionCode": Vars.cfg.data['versionCode'],
                "readState": "readahead",
                "updateTime": int(time.time()),
                "token": Vars.cfg.data.get("token")
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
            # content_info = template.ContentInfo(**response)  # create content info
            # if content_info.content:
            #     database.session.add(
            #         database.ChapterInfoSql(
            #             novel_id=novel_id,
            #             chapter_id=chapter_id,
            #             chapter_name=content_info.chapterName,
            #             chapter_content=lib.encrypt_aes(content_info.content)
            #         )
            #     )
            # with open(cache_file_path, "w", encoding="utf-8") as f:
            #     f.write(content_info.chapterName + "\n")
            #     [f.write(i + "\n") for i in content_info.content.split("\n") if i.strip() != ""]
        else:
            return response.get("message")


class Book:
    @staticmethod
    def novel_basic_info(novel_id: str) -> template.BookInfo:
        return novel_basic_info(params={"novelId": novel_id})

    @staticmethod
    def get_chapter_list(novel_id: str):
        download_content = []
        chapter_list = get_chapter_list(params={"novelId": novel_id, "more": 0, "whole": 1})
        if chapter_list is not None and chapter_list.get("chapterlist"):
            for chapter in chapter_list['chapterlist']:
                chap_info = template.ChapterInfo(**chapter)
                chap_info.chaptername = re.sub(r'[\\/:*?"<>|]', '', chap_info.chaptername)

                if not database.session.query(database.ChapterSql).filter(
                        database.ChapterSql.novelId == chap_info.novelid,
                        database.ChapterSql.chapterid == chap_info.chapterid).first():
                    download_content.append(chap_info)
                # if not os.path.exists(chap_info.cache_file_path):
                #     download_content.append(chap_info)
                # if chap_info.originalPrice == 0:
                #     download_content.append(chap_info)
                # else:
                #     if Vars.cfg.data.get("token"):
                #         download_content.append(chap_info)
        return download_content

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
