import template
from rich import print
from . import UrlConstant
from lib import GET


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
