import jinjiangAPI
import catalogue
from instance import *
import threading


def exists_file(file_path: str):
    return os.path.exists(file_path)


class Book:
    def __init__(self, book_info: dict):
        self.book_info = book_info
        self.thread_list = []
        self.speed_of_progress = 0
        self.pool_sema = threading.BoundedSemaphore(Vars.cfg.data['max_thread'])
        self.book_id = book_info["novelId"]
        self.book_name = book_info["novelName"]
        self.book_author = book_info["authorName"]
        self.book_intro = book_info["novelIntroShort"]
        self.book_class = book_info["novelClass"]
        self.book_tags = book_info["novelTags"]
        self.book_tags_id = book_info["novelTagsId"]
        self.book_chapter_count = book_info["novelChapterCount"]
        self.book_is_lock = book_info["islock"]
        self.book_is_vip = book_info["isVip"]
        self.book_is_package = book_info["isPackage"]
        self.book_is_sign = book_info["isSign"]
        self.vip_chapterid = book_info["vipChapterid"]
        self.book_review_score = book_info["novelReviewScore"]
        self.book_author_say_rule = book_info["authorsayrule"]
        self.series = book_info["series"]
        self.protagonist = book_info["protagonist"]
        self.costar = book_info["costar"]
        self.other = book_info["other"]

    def book_detailed(self) -> str:
        show_book_info = "book_name:{}".format(self.book_name)
        show_book_info += "\nbook_author:{}".format(self.book_author)
        show_book_info += "\nbook_intro:{}".format(self.book_intro)
        show_book_info += "\nbook_class:{}".format(self.book_class)
        show_book_info += "\nbook_tags:{}".format(self.book_tags)
        show_book_info += "\nbook_tags_id:{}".format(self.book_tags_id)
        show_book_info += "\nchapter_count:{}".format(self.book_chapter_count)
        show_book_info += "\nbook_is_lock:{}\n\n".format(self.book_is_lock)
        print(show_book_info)
        return show_book_info

    def multi_thread_download_content(self):
        response = jinjiangAPI.Chapter.get_chapter_list(self.book_id)
        if response.get("message") is not None:
            return print(response.get("message"))
        if len(response['chapterlist']) == 0:
            return print("the catalogue is empty")
        for index, chapter in enumerate(response['chapterlist'], start=1):
            chap = catalogue.Chapter(chapter_info=chapter, index=index)
            # content_info = jinjiangAPI.Chapter.chapter_content(self.book_id, chap.chapter_id, chap.is_vip)
            if exists_file(os.path.join(Vars.config_text, chap.chapter_id + ".txt")):  # if the file exists, skip it
                continue
            # if chap.original_price > 0:
            #     continue
            self.thread_list.append(
                threading.Thread(target=self.download_content, args=(index, chap.chapter_id, chap.is_vip,))
            )  # add to queue and download in thread

        for thread in self.thread_list:  # start thread one by one and wait for all thread done
            thread.start()
        for thread in self.thread_list:  # wait for all thread to finish and join
            thread.join()
        self.thread_list.clear()  # clear thread list and thread queue

    def download_content(self, chapter_index: int, chapter_id: str, is_vip: bool):
        self.pool_sema.acquire()
        self.speed_of_progress += 1
        if is_vip == 2:
            response = jinjiangAPI.Chapter.chapter_vip_content(self.book_id, chapter_id)
            if response.get("message") is None:
                response['content'] = jinjiangAPI.decrypt(response['content'], token=True)
        else:
            response = jinjiangAPI.Chapter.chapter_content(self.book_id, chapter_id)
        if isinstance(response, dict) and response.get("message") is None:
            content_info = catalogue.Content(response)
            content_text = f"第 {chapter_index} 章: " + content_info.chapter_title
            content_text += "\n" + content_info.content.replace("&lt;br&gt;&lt;br&gt;", "\n")
            TextFile.write(
                text_path=os.path.join(Vars.config_text, chapter_id + ".txt"),
                text_content=content_text,
                mode="w"
            )
            print("{}: {}/{}".format(self.book_name, self.speed_of_progress, self.book_chapter_count), end="\r")
        else:
            if isinstance(response, dict) and "购买章节" in response.get("message"):
                print(response.get("message"))
        self.pool_sema.release()

    def download_cover(self):
        pass

    def out_text_file(self):
        config_text_file_name_list = os.listdir(Vars.config_text)
        config_text_file_name_list.sort(key=lambda x: int(x.split(".")[0]))
        out_text_path = os.path.join(Vars.out_text_file, self.book_name + ".txt")
        if os.path.exists(out_text_path):
            os.remove(out_text_path)
        for file_name in config_text_file_name_list:
            if file_name.endswith(".txt"):
                TextFile.write(
                    text_path=out_text_path, mode="a",
                    text_content="\n\n\n" + TextFile.read(os.path.join(Vars.config_text, file_name))
                )
        print("out text file done! path:", out_text_path)

    def mkdir_content_file(self):
        Vars.config_text = os.path.join("configs", self.book_name)
        Vars.out_text_file = os.path.join("downloads", self.book_name)
        if not os.path.exists(Vars.config_text):
            os.makedirs(Vars.config_text)
        if not os.path.exists(Vars.out_text_file):
            os.makedirs(Vars.out_text_file)
