import argparse
import src
from instance import *
import book


def shell_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--id", dest="downloadbook", nargs=1, default=None, help="please input book_id")
    parser.add_argument("-s", "--search", dest="search", nargs=1, default=None, help="search book by book name")
    parser.add_argument("-m", "--max", dest="threading_max", default=None, help="please input max threading")
    parser.add_argument("-up", "--update", dest="update", default=False, action="store_true", help="update books")
    parser.add_argument("-clear", "--clear_cache", dest="clear_cache", default=False, action="store_true")
    parser.add_argument("-l", "--login", default=None, nargs="+", help="login account")
    args = parser.parse_args()

    if args.login:
        if len(args.login) >= 2:
            login_account(args.login[0], args.login[1])
        else:
            print("login failed, please input username and password")

    if args.update:
        if Vars.cfg.data['downloaded_book_id_list'] > 0:
            for book_id in Vars.cfg.data['downloaded_book_id_list']:
                if str(book_id).isdigit():
                    get_book_info(book_id)
                else:
                    print("book_id is not digit:", book_id)
        else:
            print("no book downloaded, please download book first.")

    if args.search:
        if args.search[0] != '':
            search_book(args.search[0])
        else:
            print("search book name is empty")

    if args.threading_max:
        if str(args.max).isdigit():
            Vars.threading_max = int(args.max)
            Vars.cfg.save()
        else:
            print("threading_max is not digit:", args.max)

    if args.clear_cache:
        Vars.cfg.data.clear()
        Vars.cfg.save()

    if args.downloadbook:
        get_book_info(args.downloadbook[0])


def get_book_info(bookid: str):
    Vars.current_book = src.app.Book.novel_basic_info(get_id(bookid))  # get book information by novel_id
    if Vars.current_book.get("message") is None:  # get book information success then print book information.
        Vars.current_book = book.Book(Vars.current_book)  # create book object from book information.
        Vars.current_book.start_download_book_and_get_detailed()  # start download book
        print(Vars.current_book.book_detailed)  # print book information with book detail.
        if Vars.current_book.multi_thread_download_content():  # download book content with multi thread.
            Vars.current_book.show_download_results()  # show download results after download.
            Vars.current_book.out_put_text_file()  # output book content to text file.
            Vars.current_book.set_downloaded_book_id_in_list()  # set book id in downloaded book list.
        else:
            print(f"download bookid:{bookid} failed, please try again.")
    else:
        print(Vars.current_book["message"])  # print book information error.


def search_book(search_name: str, next_page: int = 0):
    if search_name is None:
        return False
    response = src.app.Book.search_info(keyword=search_name, page=next_page)
    if response.get("code") == '200':
        for index, book_info in enumerate(response["data"]):
            print("index:", index, "novelId:", book_info["novelId"], "novelName:", book_info["novelName"])
        print("next page:[next or n]\t previous page:[previous or p], exit:[exit or e]")
        input_index = input("please input search index:")
        if str(input_index).isdigit() and int(input_index) < len(response["data"]):
            get_book_info(response["data"][int(input_index)]["novelId"])
        elif input_index == "next" or input_index == "n":
            search_book(search_name=search_name, next_page=next_page + 1)
        elif input_index == "previous" or input_index == "p":
            if next_page > 0:
                search_book(search_name=search_name, next_page=next_page - 1)
            else:
                print("no previous page!")
        elif input_index == "exit" or input_index == "e":
            return False
        else:
            print("input index is not digit or out of range, please input again.")
    else:
        print("search failed", response["message"])


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
