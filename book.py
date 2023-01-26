import src
from instance import *
import threading
from rich import print
import template


class Book:
    def __init__(self, book_info: template.BookInfo):
        self.thread_list = []
        self.pbar = None
        self.book_detailed = ""
        self.not_purchased_list = []
        self.download_successful_list = []
        self.book_info = book_info
        # self.pool_sema = threading.BoundedSemaphore(Vars.cfg.data['max_thread'])
        self.lock = threading.Lock()

    @property
    def descriptors(self) -> str:
        return self.book_info.novelIntro.replace("&lt;", "").replace("&gt;", "").replace("br/", "")

    def start_download_book_and_get_detailed(self):
        self.book_detailed = "[info]书籍名称:{}".format(self.book_info.novelName)
        self.book_detailed += "\n[info]书籍作者:{}".format(self.book_info.authorName)
        self.book_detailed += "\n[info]书籍分类:{}".format(self.book_info.novelClass)
        self.book_detailed += "\n[info]书籍标签:{}".format(self.book_info.novelTags)
        self.book_detailed += "\n[info]章节总数:{}".format(self.book_info.novelChapterCount)
        # self.book_detailed += "\n[info]书籍简介:{}".format(self.descriptors)

        self.mkdir_content_file()  # create book content file.
        # if not os.path.exists(os.path.join(Vars.config_text, self.book_info.novelId + ".jpg")):
        #     pass
        # png_file = src.request.get(
        #     url=self.book_info.get("originalCover") if self.book_info.get("originalCover") else
        #     self.book_info.get("novelCover"),
        #     return_type="content", app_url=False
        # )  # download book cover if not exists in the config_text folder
        # open(os.path.join(Vars.config_text, self.book_info.novelId + ".jpg"), "wb").write(png_file)
        # else:
        #     print("the cover is exists, skip it")  # if the cover exists, skip it

    def download_no_vip_content(self, chapter_info: template.ChapterInfo):
        response = src.app.Chapter.chapter_content(self.book_info.novelId, chapter_info.chapterid)
        content_info = template.ContentInfo(**response)  # create content info
        if content_info.content:
            with open(chapter_info.cache_file_path, "w", encoding="utf-8") as f:
                f.write(content_info.chapterName + "\n")
                for i in content_info.content.split("\n"):
                    if i.strip() != "":
                        f.write(i + "\n")
        else:
            print("get " + chapter_info.chaptername + " failed, message:", response.get("message"))

    def download_vip_content(self, chapter_info: template.ChapterInfo):
        if Vars.cfg.data.get("user_info").get("token") == "":
            print("you need login first to download vip chapter")
            return False
        if chapter_info.isvip == 2:
            response = src.app.Chapter.chapter_vip_content(self.book_info.novelId, chapter_info.chapterid)
            if response.get("message") is None:
                content_info = template.ContentInfo(**response)
                content_info.content = src.decode.decrypt(content_info.content, token=True)
                with open(chapter_info.cache_file_path, "w", encoding="utf-8") as f:
                    f.write(content_info.chapterName + "\n")
                    for i in content_info.content.split("\n"):
                        if i.strip() != "":
                            f.write(i + "\n")

    # def show_download_results(self):  # show the download results
    #     print("successful download chapter:", len(self.download_successful_list))
    #     print("Not Purchased Chapter length:", len(self.not_purchased_list))
    #     for chapter_index, chapter_info in enumerate(self.not_purchased_list):
    #         print(
    #             "顺序:", chapter_index,
    #             "\t原价:", chapter_info.get("originalPrice"),
    #             "\t章节名称:", chapter_info.get("chapterName")
    #         )

    def mkdir_content_file(self):
        Vars.out_text_file = os.path.join(Vars.cfg.data['out_path'], self.book_info.novelName)

        if not os.path.exists(Vars.current_command.cache):
            os.makedirs(Vars.current_command.cache)
        if not os.path.exists(Vars.out_text_file):
            os.makedirs(Vars.out_text_file)

    def set_downloaded_book_id_in_list(self):
        if isinstance(Vars.cfg.data['downloaded_book_id_list'], list):
            if self.book_info.novelId not in Vars.cfg.data['downloaded_book_id_list']:
                Vars.cfg.data['downloaded_book_id_list'].append(self.book_info.novelId)
                Vars.cfg.save()
            return True
        Vars.cfg.data['downloaded_book_id_list'] = [self.book_info.novelId]
        Vars.cfg.save()
