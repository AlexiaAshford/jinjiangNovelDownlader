import database
import lib
import src
import hashlib
import template
import threading
from rich import print


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

    def download_content(self, chapter_info: template.ChapterInfo, pbar):
        pbar.update(1)
        response = src.Chapter.chapter_content(self.book_info.novelId, chapter_info.chapterid, chapter_info.isvip)
        if isinstance(response, template.ContentInfo):
            # if chapter_info.isvip == 2:
            #     response.content = lib.decode.decrypt(response.content, token=True)

            if response.content:
                response.content = lib.decode.decrypt(response.content, token=True)
                # max_id = database.session.query(database.func.max(database.ChapterInfoSql.id)).scalar()
                # if max_id is None:
                #     max_id = 0
                md5 = hashlib.md5()
                md5.update(chapter_info.chaptername.encode('utf-8') + chapter_info.novelid.encode('utf-8'))

                database.session.add(
                    database.ChapterSql(
                        id=md5.hexdigest(),
                        novelId=chapter_info.novelid,
                        chapterid=chapter_info.chapterid,
                        chapter_name=chapter_info.chaptername,
                        chapter_content=lib.encrypt_aes(response.content)
                    )
                )
            self.download_successful_list.append([chapter_info, response])
        elif isinstance(response, str):
            self.download_failed_list.append([chapter_info, response])
        else:

            print("chapter is not free or vip, log:{}".format(chapter_info.isvip))

    # def set_downloaded_book_id_in_list(self):
    #     if isinstance(Vars.cfg.data['downloaded_book_id_list'], list):
    #         if self.book_info.novelId not in Vars.cfg.data['downloaded_book_id_list']:
    #             Vars.cfg.data['downloaded_book_id_list'].append(self.book_info.novelId)
    #             Vars.cfg.save()
    #         return True
    #     Vars.cfg.data['downloaded_book_id_list'] = [self.book_info.novelId]
    #     Vars.cfg.save()
