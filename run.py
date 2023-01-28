import time
import src
import book
import argparse
import template
from instance import *

from prettytable import PrettyTable
from lib import get_book_id_by_url

from concurrent.futures import ThreadPoolExecutor


def shell_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--download", nargs=1, default=None, help="please input book_id")
    parser.add_argument("-s", "--search", dest="search", nargs=1, default=None, help="search book by book name")
    parser.add_argument("--max", default=32, help="please input max threading")
    parser.add_argument("--update", default=False, action="store_true", help="update books")
    parser.add_argument("--login", default=None, nargs="+", help="login account")
    parser.add_argument("--epub", default=True, action="store_true", help="output epub file")
    parser.add_argument("--output", default="downloads", nargs="?", help="output epub file")
    parser.add_argument("--cache", default="cache", nargs="?", help="output epub file")

    Vars.current_command = parser.parse_args()
    if Vars.current_command.login:
        if len(Vars.current_command.login) >= 2:
            login_account(Vars.current_command.login[0], Vars.current_command.login[1])
        else:
            print("login failed, please input username and password")

    if Vars.current_command.update:
        if Vars.cfg.data['downloaded_book_id_list'] > 0:
            for book_id in Vars.cfg.data['downloaded_book_id_list']:
                shell_get_book_info(book_id)
        else:
            print("no book downloaded, please download book first.")

    if Vars.current_command.search:
        if Vars.current_command.search[0] != '':
            search_book(Vars.current_command.search[0])
        else:
            print("search book name is empty")

    if Vars.current_command.download:
        shell_get_book_info(Vars.current_command.download[0])


@get_book_id_by_url()
def shell_get_book_info(bookid: str):
    Vars.current_book = src.Book.novel_basic_info(bookid)
    # print(Vars.current_book.novelCover)
    if Vars.current_book is None:
        return print("bookid is not exist:", bookid)

    if not os.path.exists(f"{Vars.current_command.output}/{Vars.current_book.novelName}"):
        os.makedirs(f"{Vars.current_command.output}/{Vars.current_book.novelName}")
    if not os.path.exists(Vars.current_command.cache):
        os.makedirs(Vars.current_command.cache)

    current_book_obj = download_chapter(Vars.current_book)
    if current_book_obj:
        # clear output file information and write new description.
        with open(f"{Vars.current_command.output}/{Vars.current_book.novelName}/{Vars.current_book.novelName}.txt", "w",
                  encoding="utf-8") as f:
            f.write(f"{current_book_obj.book_detailed}\n\n\n")

        output_text_and_epub_file(Vars.current_book, get_cache_file_name(Vars.current_book))


def download_chapter(book_info):
    current_book_obj = book.Book(book_info)  # create book object from book information.
    current_book_obj.set_downloaded_book_id_in_list()  # add book id to downloaded book id list.
    print(current_book_obj.book_detailed)
    get_chapter_list = src.Book.get_chapter_list(book_info.novelId)
    if get_chapter_list is not None:
        with ThreadPoolExecutor(max_workers=Vars.current_command.max) as executor:
            for chapter in get_chapter_list:  # type: template.ChapterInfo
                if chapter.isvip == 0:
                    executor.submit(current_book_obj.download_no_vip_content, chapter)
                else:
                    # vip chapter isvip is 2
                    executor.submit(current_book_obj.download_vip_content, chapter)

        time.sleep(1)  # wait for all thread finish.
        return current_book_obj


def get_cache_file_name(book_info):
    set_file_name_list = []
    for file_name in os.listdir(Vars.current_command.cache):
        if file_name.find(book_info.novelId) != -1:
            set_file_name_list.append(file_name)

    set_file_name_list.sort(key=lambda x: int(x.split("-")[1]))  # sort file name by chapter id number.
    return set_file_name_list


def output_text_and_epub_file(book_info, file_name_list):
    with open(f"{Vars.current_command.output}/{book_info.novelName}/{book_info.novelName}.txt", "a",
              encoding="utf-8") as f2:
        for index, file_name in enumerate(file_name_list, start=1):
            with open(f"{Vars.current_command.cache}/{file_name}", "r", encoding="utf-8") as f:
                # content = f.read()
                # chapter_title = content.split("\n")[0]
                f2.write(f"\n\n\n第{index}章 " + f.read())

    command_line = f"-file {Vars.current_command.output}/{book_info.novelName}/{book_info.novelName}.txt " \
                   f"-o {Vars.current_command.output}/{book_info.novelName} " \
                   f"-cover {book_info.novelCover}"

    if Vars.current_command.epub:
        if os.name == 'nt':
            os.system(f"epub_windows_x64.exe " + command_line)
        elif os.name == 'posix':
            os.system(f"./epub_linux_x64 " + command_line)
        else:
            print("not support os, please use windows or linux x64")
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
    novel_info_list = src.Book.search_info(keyword=search_name, page=next_page)

    table = PrettyTable(['序号', '书号', '书名', '作者'])
    for index, novel_info in enumerate(novel_info_list):
        table.add_row([str(index), novel_info.novel_id, novel_info.novel_name, novel_info.author_name])
    print(table)
    print("next page:[next or n]\t previous page:[previous or p], exit:[exit or e], input index to download.")
    while True:
        input_index = input(">")
        if input_index.isdigit() and int(input_index) < len(novel_info_list):
            break
        elif input_index == "next" or input_index == "n":
            return search_book(search_name, next_page + 1)
        elif input_index == "previous" or input_index == "p":
            return search_book(search_name, next_page - 1)
        elif input_index == "exit" or input_index == "e":
            return
    shell_get_book_info(novel_info_list[int(input_index)].novel_id)


def login_account(username: str, password: str):
    response = src.app.Account.login(username, password)
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
    try:
        shell_parser()
    except KeyboardInterrupt:
        print("\n exit program by keyboard interrupt")
