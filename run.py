import argparse
import jinjiangAPI
from instance import *
import book


def shell_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--id", dest="downloadbook", nargs=1, default=None, help="please input book_id")
    parser.add_argument("-m", "--max", dest="threading_max", default=None, help="please input max threading")
    parser.add_argument("-up", "--update", dest="update", default=False, action="store_true", help="update books")
    parser.add_argument("-clear", "--clear_cache", dest="clear_cache", default=False, action="store_true")
    parser.add_argument("-l", "--login", default=None, dest="account", help="login account")
    args = parser.parse_args()
    if args.account:
        login_account(args.account)

    if args.update:
        # shell_update()
        pass

    if args.clear_cache:
        Vars.cfg.data.clear()
        Vars.cfg.save()

    if args.threading_max:
        Vars.cfg.data['max_thread'] = int(args.max)

    if args.downloadbook:
        get_book_info(args.downloadbook[0])


def get_book_info(bookid: str):
    if bookid is not None:
        Vars.current_book = jinjiangAPI.Book.novel_basic_info(get_id(bookid))  # get book information by novel_id
        if Vars.current_book.get("message") is None:  # get book information success then print book information.
            Vars.current_book = book.Book(Vars.current_book)  # create book object from book information.
            Vars.current_book.show_book_detailed()  # print book information with book detail.
            Vars.current_book.mkdir_content_file()  # create book content file.
            Vars.current_book.download_book_cover()  # download book cover.
            if Vars.current_book.multi_thread_download_content():  # download book content with multi thread.
                Vars.current_book.out_text_file()  # output book content to text file.
        else:
            print(Vars.current_book["message"])  # print book information error.


def login_account(account: str):
    if account is None:
        return False
    if "----" in account:  # if account is a ----, then use default account and password
        username, password = account.split("----")
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
