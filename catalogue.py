class Chapter:
    def __init__(self, chapter_info: dict, index: int = 0):
        self.index = index
        self.chapter_info = chapter_info
        self.chapter_id = chapter_info["chapterid"]
        self.chapter_name = chapter_info["chaptername"]
        self.chapter_date = chapter_info["chapterdate"]
        self.chapter_click = chapter_info["chapterclick"]
        self.chapter_size = chapter_info["chaptersize"]
        self.chapter_intro = chapter_info["chapterintro"]
        self.is_lock = chapter_info["islock"]
        self.is_vip = chapter_info["isvip"]
        self.point = chapter_info["point"]
        self.original_price = chapter_info["originalPrice"]
        self.pointfree_vip = chapter_info["pointfreevip"]
        self.is_protect = chapter_info["isProtect"]
        self.original_price_message = chapter_info["originalPriceMessage"]
        self.point_message = chapter_info["pointMeassge"]
        self.chapter_message = chapter_info["chapterMessage"]
        self.lastpost_time = chapter_info["lastpost_time"]
        self.is_edit = chapter_info["isEdit"]

    def __str__(self) -> str:
        show_chapter_info = "chapter_name:{}".format(self.chapter_name)
        show_chapter_info += "\nchapter_date:{}".format(self.chapter_date)
        show_chapter_info += "\nchapter_click:{}".format(self.chapter_click)
        show_chapter_info += "\nchapter_size:{}".format(self.chapter_size)
        show_chapter_info += "\nchapter_intro:{}".format(self.chapter_intro)
        show_chapter_info += "\nis_lock:{}".format(self.is_lock)
        show_chapter_info += "\nis_vip:{}".format(self.is_vip)
        show_chapter_info += "\npoint:{}".format(self.point)
        show_chapter_info += "\noriginal_price:{}".format(self.original_price)
        show_chapter_info += "\npointfree_vip:{}".format(self.pointfree_vip)
        show_chapter_info += "\nis_protect:{}".format(self.is_protect)
        show_chapter_info += "\noriginal_price_message:{}".format(self.original_price_message)
        show_chapter_info += "\npoint_message:{}".format(self.point_message)
        show_chapter_info += "\nchapter_message:{}".format(self.chapter_message)
        show_chapter_info += "\nlastpost_time:{}".format(self.lastpost_time)
        show_chapter_info += "\nis_edit:{}".format(self.is_edit)
        return show_chapter_info


class Content:
    def __init__(self, content_info: dict):
        self.content_info = content_info
        self.chapter_id = content_info["chapterId"]
        self.chapter_name = content_info["chapterName"]
        self.chapter_intro = content_info["chapterIntro"]
        self.chapter_size = content_info["chapterSize"]
        self.chapter_date = content_info["chapterDate"]
        self.say_body = content_info["sayBody"]
        self.content = content_info["content"]
        self.is_vip = content_info["isvip"]
        self.author_id = content_info["authorid"]
        self.autobuy_status = content_info["autobuystatus"]

    def __str__(self) -> str:
        show_content_info = "chapter_id:{}".format(self.chapter_id)
        show_content_info += "\nchapter_name:{}".format(self.chapter_name)
        show_content_info += "\nchapter_intro:{}".format(self.chapter_intro)
        show_content_info += "\nchapter_size:{}".format(self.chapter_size)
        show_content_info += "\nchapter_date:{}".format(self.chapter_date)
        show_content_info += "\nsay_body:{}".format(self.say_body)
        show_content_info += "\ncontent:{}".format(self.content)
        show_content_info += "\nis_vip:{}".format(self.is_vip)
        show_content_info += "\nauthor_id:{}".format(self.author_id)
        show_content_info += "\nautobuy_status:{}".format(self.autobuy_status)
        return show_content_info
