import jinjiangAPI
import catalogue
from instance import *
import threading


class Book:
    def __init__(self, book_info: dict):
        self.book_info = book_info
        self.thread_list = []
        self.speed_of_progress = 0
        self.book_detailed = ""
        self.not_purchased_list = []
        self.download_successful_list = []
        self.book_id = book_info["novelId"]
        self.book_name = book_info["novelName"]
        self.book_author = book_info["authorName"]
        self.book_class = book_info["novelClass"]
        self.book_tags = book_info["novelTags"]
        self.book_is_lock = book_info["islock"]
        self.book_is_vip = book_info["isVip"]
        self.book_is_package = book_info["isPackage"]
        self.book_is_sign = book_info["isSign"]
        self.protagonist = book_info["protagonist"]
        self.vip_chapterid = book_info["vipChapterid"]
        self.book_intro = book_info["novelIntroShort"]
        self.book_review_score = book_info["novelReviewScore"]
        self.book_author_say_rule = book_info["authorsayrule"]
        self.book_chapter_count = book_info["novelChapterCount"]
        self.pool_sema = threading.BoundedSemaphore(Vars.cfg.data['max_thread'])

    def start_download_book_and_get_detailed(self):
        self.book_detailed = "[info]书籍名称:{}".format(self.book_name)
        self.book_detailed += "\n[info]书籍作者:{}".format(self.book_author)
        self.book_detailed += "\n[info]书籍分类:{}".format(self.book_class)
        self.book_detailed += "\n[info]书籍标签:{}".format(self.book_tags)
        self.book_detailed += "\n[info]章节总数:{}".format(self.book_chapter_count)
        self.book_detailed += "\n[info]书籍简介:{}".format(self.book_intro)

        self.mkdir_content_file()  # create book content file.
        if not os.path.exists(os.path.join(Vars.config_text, self.book_id + ".jpg")):
            png_file = jinjiangAPI.get(
                url=self.book_info.get("originalCover") if self.book_info.get("originalCover") else
                self.book_info.get("novelCover"),
                return_type="content", app_url=False
            )  # download book cover if not exists in the config_text folder
            open(os.path.join(Vars.config_text, self.book_id + ".jpg"), "wb").write(png_file)
        else:
            print("the cover is exists, skip it")  # if the cover exists, skip it

    def multi_thread_download_content(self):
        response = jinjiangAPI.Chapter.get_chapter_list(self.book_id)
        if response.get("message") is not None:  # if the book is not exist or the book is locked by jinjiang server
            return print(response.get("message"))
        if len(response['chapterlist']) == 0:  # if the book chapter list is empty
            return print("the catalogue is empty")
        for index, chapter in enumerate(response['chapterlist'], start=1):
            chap = catalogue.Chapter(chapter_info=chapter, index=index)
            if os.path.exists(os.path.join(Vars.config_text, chap.chapter_id + ".txt")):  # if the file exists, skip it
                continue  # skip the chapter if the file exists
            self.thread_list.append(
                threading.Thread(target=self.download_content, args=(index, chap,))
            )  # add to queue and download in thread

        for thread in self.thread_list:  # start thread one by one and wait for all thread done
            thread.start()
        for thread in self.thread_list:  # wait for all thread to finish and join
            thread.join()
        self.thread_list.clear()  # clear thread list and thread queue
        return True  # all thread done and clear thread list and thread queue

    def download_content(self, chapter_index: int, chapter_info: catalogue.Chapter):
        self.pool_sema.acquire()
        self.speed_of_progress += 1
        if chapter_info.is_vip == 2 and chapter_info.original_price > 0:
            if Vars.cfg.data.get("user_info").get("token") == "":
                print("you need login first to download vip chapter")
                self.pool_sema.release()
                return False
            response = jinjiangAPI.Chapter.chapter_vip_content(self.book_id, chapter_info.chapter_id)
            if response.get("message") is None:
                response['content'] = jinjiangAPI.decrypt(response['content'], token=True)
                self.download_successful_list.append(chapter_info)
            else:
                self.pool_sema.release()
                self.not_purchased_list.append(response)  # if the chapter is vip add to not_purchased_list
                return False
        else:
            response = jinjiangAPI.Chapter.chapter_content(self.book_id, chapter_info.chapter_id)

        if isinstance(response, dict) and response.get("message") is None:
            content_info = catalogue.Content(response)
            content_title = f"第 {chapter_index} 章: " + content_info.chapter_title
            File.write(
                text_path=os.path.join(Vars.config_text, chapter_info.chapter_id + ".txt"),
                text_content=content_title + "\n" + content_info.content, mode="w"
            )
            print("{}: {}/{}".format(self.book_name, self.speed_of_progress, self.book_chapter_count), end="\r")
        else:
            if isinstance(response, dict) and "购买章节" in response.get("message"):
                print("download_content:", response.get("message"))
        self.download_successful_list.append(response)
        self.pool_sema.release()

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
        config_text_file_name_list = os.listdir(Vars.config_text)
        config_text_file_name_list.sort(key=lambda x: int(x.split(".")[0]))  # sort by chapter index number
        File.write(
            text_path=os.path.join(Vars.out_text_file, self.book_name + ".txt"),
            mode="w", text_content=self.book_detailed
        )  # write book info to file
        for file_name in config_text_file_name_list:
            if file_name.endswith(".txt"):
                File.write(text_path=os.path.join(Vars.out_text_file, self.book_name + ".txt"),
                           text_content="\n\n\n" + File.read(os.path.join(Vars.config_text, file_name)))

        print("out text file done! path:", os.path.join(Vars.out_text_file, self.book_name + ".txt"))

    def mkdir_content_file(self):
        Vars.config_text = os.path.join(Vars.cfg.data['config_path'], self.book_name)
        Vars.out_text_file = os.path.join(Vars.cfg.data['out_path'], self.book_name)
        if not os.path.exists(Vars.config_text):
            os.makedirs(Vars.config_text)
        if not os.path.exists(Vars.out_text_file):
            os.makedirs(Vars.out_text_file)

    def set_downloaded_book_id_in_list(self):
        if isinstance(Vars.cfg.data['downloaded_book_id_list'], list):
            if self.book_id not in Vars.cfg.data['downloaded_book_id_list']:
                Vars.cfg.data['downloaded_book_id_list'].append(self.book_id)
                Vars.cfg.save()
            return True
        Vars.cfg.data['downloaded_book_id_list'] = [self.book_id]
        Vars.cfg.save()
