import jinjiangAPI


def login_account(username: str, password: str) -> dict:
    response = jinjiangAPI.Account.login(username, password)
    if response.get("message") is None:
        print("login success", response["nickName"], "vip:", response["readergrade"])
        return {"readerId": response["readerId"], "token": response["token"]}
    else:
        print("login failed", response["message"])


if __name__ == '__main__':
    username, password = "", ""
    login_account(username, password)
