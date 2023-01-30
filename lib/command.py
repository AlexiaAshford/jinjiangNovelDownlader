import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--download", nargs=1, default=None, help="please input book_id")
    parser.add_argument("-s", "--search", dest="search", nargs=1, default=None, help="search book by book name")
    parser.add_argument("--token", default=None, help="add token")
    parser.add_argument("--max", default=32, help="please input max threading")
    parser.add_argument("--update", default=False, action="store_true", help="update books")
    parser.add_argument("--login", default=None, nargs="+", help="login account")
    parser.add_argument("--epub", default=True, action="store_true", help="output epub file")
    parser.add_argument("--output", default="downloads", nargs="?", help="output epub file")
    # parser.add_argument("--cache", default="cache", nargs="?", help="output epub file")
    parser.add_argument("--update_database", default=False, action="store_true", help="update database")

    return parser.parse_args()
