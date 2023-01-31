import base64

import lib
import src
import book
import argparse
import template
import database
from instance import *
from tqdm import tqdm
from prettytable import PrettyTable
from lib import get_book_id_by_url, parse_args

from concurrent.futures import ThreadPoolExecutor


def shell_command():
    if Vars.current_command.token:
        Vars.cfg.data['token'] = Vars.current_command.token
        Vars.cfg.save()
    if Vars.current_command.login:
        if len(Vars.current_command.login) >= 2:
            login_account(Vars.current_command.login[0], Vars.current_command.login[1])
        else:
            print("login failed, please input username and password")

    if Vars.current_command.update:
        results = database.session.query(database.BookInfoSql).filter().all()
        if len(results) > 1:
            table = PrettyTable()
            table.field_names = ["序号", "书名", "作者", "章节数"]
            for result in results:  # type: database.BookInfoSql
                table.add_row([result.novelId, result.novelName, result.authorName, result.novelChapterCount])
            print(table)
            for result in results:
                shell_get_book_info(result.novelId)

    if Vars.current_command.search:
        if Vars.current_command.search[0] != '':
            search_book(Vars.current_command.search[0])
        else:
            print("search book name is empty")

    if Vars.current_command.download:
        shell_get_book_info(Vars.current_command.download[0])


@get_book_id_by_url()
def shell_get_book_info(bookid: str):
    filter_info = database.session.query(database.BookInfoSql).filter(database.BookInfoSql.novelId == bookid).first()
    if not filter_info or Vars.current_command.update_database:
        print("check database not exist book information, get information from server api.")
        Vars.current_book = src.Book.novel_basic_info(bookid)
        if Vars.current_book is None:
            return print("bookid is not exist:", bookid)
        database.session.add(database.BookInfoSql(**Vars.current_book.dict()))
        database.session.commit()
    else:
        print("check database exist book information, not get information from server api.")
        # delete sqlalchemy object attribute.
        filter_info.__dict__.pop("_sa_instance_state")
        Vars.current_book = template.BookInfo(**filter_info.__dict__)

    if not os.path.exists(f"{Vars.current_command.output}/{Vars.current_book.novelName}"):
        os.makedirs(f"{Vars.current_command.output}/{Vars.current_book.novelName}")

    current_book_obj = download_chapter(Vars.current_book)
    if current_book_obj:
        # clear output file information and write new description.
        with open(f"{Vars.current_command.output}/{Vars.current_book.novelName}/{Vars.current_book.novelName}.txt", "w",
                  encoding="utf-8") as f:
            f.write(f"{current_book_obj.book_detailed}\n\n\n")

        output_text_and_epub_file(Vars.current_book)


def download_chapter(book_info):
    current_book_obj = book.Book(book_info)  # create book object from book information.
    # current_book_obj.set_downloaded_book_id_in_list()  # add book id to downloaded book id list.
    print(current_book_obj.book_detailed)
    if current_book_obj.book_info.novelChapterCount == 0:
        print("book chapter is empty.")
        return None
    get_chapter_list = src.Book.get_chapter_list(book_info.novelId)
    if get_chapter_list is not None:
        new_tqdm = tqdm(total=len(get_chapter_list), desc="下载进度", ncols=100)
        # with ThreadPoolExecutor(max_workers=Vars.current_command.max) as executor:
        #     for chapter in get_chapter_list:  # type: template.ChapterInfo
        #         executor.submit(current_book_obj.download_content, chapter, new_tqdm)

        for chapter in get_chapter_list:  # type: template.ChapterInfo
            current_book_obj.download_content(chapter, new_tqdm)
        # time.sleep(1)  # wait for all thread finish.
        new_tqdm.close()
        try:
            database.session.commit()
        except Exception as e:
            print("commit database error:", e)
            database.session.rollback()
        print("一共 {} 章下载失败".format(len(current_book_obj.download_failed_list)))
        table = PrettyTable(['序号', '章节名', '是否上架', '错误原因'])
        for failed_chapter in current_book_obj.download_failed_list:
            table.add_row([failed_chapter[0].chapterid, failed_chapter[0].chaptername,
                           "免费" if failed_chapter[0].isvip == 0 else "付费",
                           failed_chapter[1]])
        print(table)
        return current_book_obj


# def get_cache_file_name(book_info):
#     set_file_name_list = []
#     for file_name in os.listdir(Vars.current_command.cache):
#         if file_name.find(book_info.novelId) != -1:
#             set_file_name_list.append(file_name)
#
#     set_file_name_list.sort(key=lambda x: int(x.split("-")[1]))  # sort file name by chapter id number.
#     return set_file_name_list


def output_text_and_epub_file(book_info):
    chapter_list = database.session.query(database.ChapterSql).filter(
        database.ChapterSql.novelId == book_info.novelId).all()

    chapter_list.sort(key=lambda x: int(x.chapterid))  # sort chapter list by chapter id number.
    with open(f"{Vars.current_command.output}/{book_info.novelName}/{book_info.novelName}.txt", "a",
              encoding="utf-8") as f2:
        for chapter in chapter_list:  # type: database.ChapterSql
            chapter_name = f"\n\n\n第{chapter.chapterid}章: " + chapter.chapter_name
            # print(chapter.chapter_content)
            f2.write(chapter_name + "\n\n" + lib.decrypt_aes(chapter.chapter_content))

    command_line = f"-file {Vars.current_command.output}/{book_info.novelName}/{book_info.novelName}.txt " \
                   f"-o {Vars.current_command.output}/{book_info.novelName} " \
                   f"-cover \"{book_info.novelCover}\" " \
                   f"-cover_name {book_info.novelId}"

    if Vars.current_command.epub:
        if os.name == 'nt':
            os.system(f"epub_windows_x64.exe " + command_line)
        elif os.name == 'posix':
            os.system(f"./epub_linux_x64 " + command_line)
        else:
            print("not support os, please use windows or linux x64,create epub file failed.")
        # epub_book.epub_file_export()
        # current_book.show_download_results()  # show download results after download.
        # current_book.out_put_text_file()  # output book content to text file.
        # current_book.set_downloaded_book_id_in_list()  # set book id in downloaded book list.
        #
        # if current_book.multi_thread_download_content():  # download book content with multi thread.
        #     current_book.show_download_results()  # show download results after download.
        #     current_book.out_put_text_file()  # output book content to text file.
        #     current_book.set_downloaded_book_id_in_list()  # set book id in downloaded book list.
        # else:
        #     print(f"download bookid:{bookid} failed, please try again.")


def search_book(search_name: str, next_page: int = 1):
    book_id = src.Book.search_info(keyword=search_name, page=next_page)
    if book_id is not None:
        shell_get_book_info(book_id)


def login_account(username: str, password: str):
    response = src.Account.login(username, password)
    if response.get("message") is None:
        print("login success", response["nickName"], "vip:", response["readergrade"])
        Vars.cfg.data['user_info'] = {
            "nickName": response["nickName"],
            "token": response["token"],
            "readerId": response["readerId"],
            "balance": response["balance"],
            "readergrade": response["readergrade"]
        }
        Vars.cfg.save()
    else:
        print("login failed", response["message"])


if __name__ == '__main__':
    set_config()
    # init command line arguments.
    Vars.current_command = parse_args()
    database.session.execute("CREATE INDEX IF NOT EXISTS chapter_index ON chapterinfo (novelId);")
    if not src.Account.user_center():
        print("[err]test your account failed, please input your valid token.")

    shell_command()
