import src
from instance import *
import threading
from rich import print
import template


class Book:
    def __init__(self, book_info: template.BookInfo):
        self.thread_list = []
        self.pbar = None
        self.not_purchased_list = []
        self.download_successful_list = []
        self.book_info = book_info
        self.download_failed_list = []
        self.lock = threading.Lock()

    @property
    def descriptors(self) -> str:
        return self.book_info.novelIntro.replace("&lt;", "").replace("&gt;", "").replace("br/", "")

    @property
    def book_detailed(self):
        book_detailed = "[info]书籍名称:{}".format(self.book_info.novelName)
        book_detailed += "\n[info]书籍作者:{}".format(self.book_info.authorName)
        book_detailed += "\n[info]书籍序号:{}".format(self.book_info.novelId)
        book_detailed += "\n[info]书籍分类:{}".format(self.book_info.novelClass)
        book_detailed += "\n[info]书籍标签:{}".format(self.book_info.novelTags)
        book_detailed += "\n[info]章节总数:{}".format(self.book_info.novelChapterCount)
        book_detailed += "\n[info]书籍简介:{}".format(self.descriptors)
        return book_detailed

    def download_no_vip_content(self, chapter_info: template.ChapterInfo):
        message = src.Chapter.chapter_free_content(self.book_info.novelId, chapter_info.chapterid,
                                                   chapter_info.cache_file_path)
        if isinstance(message, str):
            self.download_failed_list.append([chapter_info, message])

    def download_vip_content(self, chapter_info: template.ChapterInfo):
        if Vars.cfg.data.get("token") == "":
            print("you need login first to download vip chapter")
            return False
        if chapter_info.isvip == 2:
            message = src.Chapter.chapter_vip_content(self.book_info.novelId, chapter_info.chapterid,
                                                      chapter_info.cache_file_path)
            if isinstance(message, str):
                self.download_failed_list.append([chapter_info, message])

    def set_downloaded_book_id_in_list(self):
        if isinstance(Vars.cfg.data['downloaded_book_id_list'], list):
            if self.book_info.novelId not in Vars.cfg.data['downloaded_book_id_list']:
                Vars.cfg.data['downloaded_book_id_list'].append(self.book_info.novelId)
                Vars.cfg.save()
            return True
        Vars.cfg.data['downloaded_book_id_list'] = [self.book_info.novelId]
        Vars.cfg.save()
