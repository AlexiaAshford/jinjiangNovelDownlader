import src
from instance import *
import threading
from tqdm import tqdm
from rich import print
import tools_sqlite
import template


class Book:
    def __init__(self, book_info: template.BookInfo):
        self.thread_list = []
        self.pbar = None
        self.book_detailed = ""
        self.not_purchased_list = []
        self.download_successful_list = []
        self.book_info = book_info
        self.sql = tools_sqlite.SqliteTools("jinjiang.cache.db")
        # self.pool_sema = threading.BoundedSemaphore(Vars.cfg.data['max_thread'])
        self.lock = threading.Lock()

    @property
    def descriptors(self) -> str:
        return self.book_info.novelIntro.replace("&lt;", "").replace("&gt;", "").replace("br/", "")

    def start_download_book_and_get_detailed(self):
        self.sql.create_table("book_info", self.book_info.dict().keys(), key="novelId")
        if self.sql.get("book_info", self.book_info.novelId, key="novelId") is None:
            self.sql.insert("book_info", self.book_info.dict())
        self.book_detailed = "[info]书籍名称:{}".format(self.book_info.novelName)
        self.book_detailed += "\n[info]书籍作者:{}".format(self.book_info.authorName)
        self.book_detailed += "\n[info]书籍分类:{}".format(self.book_info.novelClass)
        self.book_detailed += "\n[info]书籍标签:{}".format(self.book_info.novelTags)
        self.book_detailed += "\n[info]章节总数:{}".format(self.book_info.novelChapterCount)
        # self.book_detailed += "\n[info]书籍简介:{}".format(self.descriptors)

        self.mkdir_content_file()  # create book content file.
        if not os.path.exists(os.path.join(Vars.config_text, self.book_info.novelId + ".jpg")):
            pass
            # png_file = src.request.get(
            #     url=self.book_info.get("originalCover") if self.book_info.get("originalCover") else
            #     self.book_info.get("novelCover"),
            #     return_type="content", app_url=False
            # )  # download book cover if not exists in the config_text folder
            # open(os.path.join(Vars.config_text, self.book_info.novelId + ".jpg"), "wb").write(png_file)
        else:
            print("the cover is exists, skip it")  # if the cover exists, skip it

    def multi_thread_download_content(self):
        response = src.app.Chapter.get_chapter_list(self.book_info.novelId)
        if response.get("message") is not None or len(response['chapterlist']) == 0:
            print("get chapter list failed, message:", response.get("message"))
            return False
        self.sql.create_table("content_info", template.ContentInfo().dict().keys(), key="chapterid")
        for index, chapter in enumerate(response['chapterlist'], start=1):
            chap = template.ChapterInfo(**chapter)
            content_info_cache = self.sql.get("content_info", str(chap.chapterid), key="chapterid")
            if content_info_cache:
                print(content_info_cache['chapterName'], "is exists, skip it")
            else:
                if chap.originalPrice == 0:
                    self.thread_list.append(threading.Thread(target=self.download_content, args=(chap,)))
        if len(self.thread_list) > 0:
            self.pbar = tqdm(total=len(self.thread_list), desc="download content", ncols=100)
            for thread in self.thread_list:  # start thread one by one and wait for all thread done
                thread.start()
            for thread in self.thread_list:  # wait for all thread to finish and join
                thread.join()
            self.thread_list.clear()  # clear thread list and thread queue
            self.pbar.close()
        return True  # all thread done and clear thread list and thread queue

    def save_content(self, response: dict):

        if isinstance(response, dict) and response.get("message") is None:
            content_info = template.ContentInfo(**response)
            self.sql.insert("content_info", content_info.dict())
            self.download_successful_list.append(response)
        else:
            if isinstance(response, dict) and "购买章节" in response.get("message"):
                print("download_content:", response.get("message"))

    def download_content(self, chapter_info: template.ChapterInfo):
        self.lock.acquire(True)
        try:
            if chapter_info.isvip == 2 and chapter_info.originalPrice > 0:
                if Vars.cfg.data.get("user_info").get("token") == "":
                    print("you need login first to download vip chapter")
                    return False
                response = src.app.Chapter.chapter_vip_content(self.book_info.novelId, chapter_info.chapterid)
                if response.get("message") is None:
                    response['content'] = src.decode.decrypt(response['content'], token=True)
                    self.download_successful_list.append(chapter_info)
                else:
                    self.not_purchased_list.append(response)  # if the chapter is vip add to not_purchased_list
                    return False
            else:
                response = src.app.Chapter.chapter_content(self.book_info.novelId, chapter_info.chapterid)
            self.save_content(response)
        finally:
            self.pbar.update(1)
            self.lock.release()

    def show_download_results(self):  # show the download results
        print("successful download chapter:", len(self.download_successful_list))
        print("Not Purchased Chapter length:", len(self.not_purchased_list))
        for chapter_index, chapter_info in enumerate(self.not_purchased_list):
            print(
                "顺序:", chapter_index,
                "\t原价:", chapter_info.get("originalPrice"),
                "\t章节名称:", chapter_info.get("chapterName")
            )

    def out_put_text_file(self):
        content_info_cache = self.sql.get_all("content_info")
        content_info_cache.sort(key=lambda x: int(x['chapterId']))

        File.write(
            text_path=os.path.join(Vars.out_text_file, self.book_info.novelName + ".txt"),
            mode="w", text_content=self.book_detailed
        )  # write book info to file
        for content_info in content_info_cache:
            content_title = f"第 {content_info['chapterId']} 章: " + content_info['chapterName']
            File.write(
                text_path=os.path.join(Vars.out_text_file, self.book_info.novelName + ".txt"),
                text_content="\n\n\n" + content_title + "\n" + content_info['content'], mode="a"
            )
        print("out text file done! path:", os.path.join(Vars.out_text_file, self.book_info.novelName + ".txt"))

    def mkdir_content_file(self):
        Vars.config_text = os.path.join(Vars.cfg.data['config_path'], self.book_info.novelName)
        Vars.out_text_file = os.path.join(Vars.cfg.data['out_path'], self.book_info.novelName)
        if not os.path.exists(Vars.config_text):
            os.makedirs(Vars.config_text)
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
