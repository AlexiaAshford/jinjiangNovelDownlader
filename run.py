import jinjiangAPI
import click
from instance import *
import book


@click.command()
@click.option('--bid', default="", help='description')  # book id (novel_id)
def get_book_info(bid: str):
    Vars.current_book = jinjiangAPI.Book.novel_basic_info(bid)  # get book information by novel_id
    if Vars.current_book.get("message") is None:  # get book information success then print book information
        Vars.current_book = book.Book(Vars.current_book)
        Vars.current_book.mkdir_content_file()
        Vars.current_book.get_catalogue()
    else:
        print(Vars.current_book["message"])


@click.command()
@click.option('--account', default="", help='description')
def login_account(account: str):
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
    # get_book_info()
    login_account()
