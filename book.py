class Book:
    def __init__(self, book_info: dict):
        self.book_info = book_info
        self.book_id = book_info["novelId"]
        self.book_name = book_info["novelName"]
        self.book_author = book_info["authorName"]
        self.book_cover = book_info["originalCover"]
        self.book_intro = book_info["novelIntroShort"]
        self.book_class = book_info["novelClass"]
        self.book_tags = book_info["novelTags"]
        self.book_tags_id = book_info["novelTagsId"]
        self.book_size = book_info["novelSize"]
        self.book_chapter_count = book_info["novelChapterCount"]
        self.book_score = book_info["novelScore"]
        self.book_is_lock = book_info["islock"]
        self.book_is_vip = book_info["isVip"]
        self.book_is_package = book_info["isPackage"]
        self.book_is_sign = book_info["isSign"]
        self.vip_chapterid = book_info["vipChapterid"]
        self.book_main_view = book_info["mainview"]
        self.book_code_url = book_info["codeUrl"]
        self.book_review_score = book_info["novelReviewScore"]
        self.book_author_say_rule = book_info["authorsayrule"]
        self.series = book_info["series"]
        self.protagonist = book_info["protagonist"]
        self.costar = book_info["costar"]
        self.other = book_info["other"]

    def __str__(self) -> str:
        show_book_info = "book_name:{}".format(self.book_name)
        show_book_info += "\nbook_author:{}".format(self.book_author)
        show_book_info += "\nbook_cover:{}".format(self.book_cover)
        show_book_info += "\nbook_intro:{}".format(self.book_intro)
        show_book_info += "\nbook_class:{}".format(self.book_class)
        show_book_info += "\nbook_tags:{}".format(self.book_tags)
        show_book_info += "\nbook_tags_id:{}".format(self.book_tags_id)
        show_book_info += "\nbook_size:{}".format(self.book_size)
        show_book_info += "\nbook_chapter_count:{}".format(self.book_chapter_count)
        show_book_info += "\nbook_score:{}".format(self.book_score)
        show_book_info += "\nbook_is_lock:{}".format(self.book_is_lock)
        return show_book_info
