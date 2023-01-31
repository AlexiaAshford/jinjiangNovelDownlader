import template
from rich import print
from . import UrlConstant
from lib import GET, CheckJsonAndAddModel


@CheckJsonAndAddModel(template.BookInfo)
@GET(UrlConstant.NOVEL_INFO)
def novel_basic_info(response: dict):  # get book information by novel_id
    return response, UrlConstant.WEB_HOST + UrlConstant.NOVEL_INFO


@GET(UrlConstant.SEARCH_INFO)
def search_home_page(response: dict) -> [dict, None]:  # search book by keyword
    if response.get("code") == '200':
        return response.get("data")
    else:
        print("search failed:", response.get("message"))


@CheckJsonAndAddModel(template.UserCenter)
@GET("getUserCenter")
def get_user_center(response: dict):
    return response, UrlConstant.WEB_HOST + UrlConstant.NOVEL_INFO


@CheckJsonAndAddModel(template.UserInfo)
@GET("getAppUserinfo")
def get_user_info(response: dict):
    return response, UrlConstant.WEB_HOST + UrlConstant.NOVEL_INFO


@GET("search")
def search_book(response: dict):  # search book by keyword
    novel_info_list = []
    if response.get("items"):
        for index, novel_info in enumerate(response.get("items")):
            novel_info_list.append(template.SearchInfo(**novel_info))
    else:
        if response.get("message") == "没有更多小说了！":
            return response.get("message")
        else:
            print("search failed:", response.get("message"))

    return novel_info_list


@CheckJsonAndAddModel()
@GET(UrlConstant.CHAPTER_LIST)
def get_chapter_list(response):  # get chapter list by novel_id
    return response, UrlConstant.WEB_HOST + UrlConstant.NOVEL_INFO


@GET("chapterContent")
def get_chapter_vip_content(response) -> dict:
    try:
        return response
    except Exception as e:
        print(e)


@GET(UrlConstant.CONTENT)
def get_chapter_free_content(response) -> dict:
    try:
        return response
    except Exception as e:
        print(e)
