import argparse
import jinjiangAPI
from instance import *
import book


def shell_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--id", dest="downloadbook", nargs=1, default=None, help="please input book_id")
    parser.add_argument("-s", "--search", dest="search", nargs=1, default=None, help="search book by book name")
    parser.add_argument("-m", "--max", dest="threading_max", default=None, help="please input max threading")
    parser.add_argument("-up", "--update", dest="update", default=False, action="store_true", help="update books")
    parser.add_argument("-clear", "--clear_cache", dest="clear_cache", default=False, action="store_true")
    parser.add_argument("-l", "--login", default=None, dest="account", help="login account")
    args = parser.parse_args()
    if args.account:
        login_account(args.account)

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
    if bookid is not None:
        Vars.current_book = jinjiangAPI.Book.novel_basic_info(get_id(bookid))  # get book information by novel_id
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


def search_book(search_name: str, next_page: dict = None):
    if search_name is None:
        return False
    response = jinjiangAPI.Book.search_info(search_name)
    if response.get("code") == '200':
        for index, book_info in enumerate(response["data"]):
            print("index:", index, "novelId:", book_info["novelId"], "novelName:", book_info["novelName"])
        input_index = input("please input search index: ")
        if str(input_index).isdigit() and int(input_index) < len(response["data"]):
            get_book_info(response["data"][int(input_index)]["novelId"])
        # elif input_index == "next":
        #     get_book_info(response["data"][0]["novelId"])
        else:
            print("input index is not digit or out of range")
    else:
        print("search failed", response["message"])


def login_account(account: str):
    if account is None:
        return False
    if "----" in account:  # if account is a ----, then use default account and password
        username, password = account.split("----")  # get username and password from account
    else:
        username, password = account.split(" ")
    response = jinjiangAPI.Account.login(username, password)
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
    shell_parser()
