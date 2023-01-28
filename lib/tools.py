import re


def get_book_id_by_url():
    def wrapper(func):
        def decorator(url: str):
            result = re.compile(r'(\d+)').findall(str(url))
            if len(result) > 0 and str(result[0]).isdigit():
                func(result[0])
            else:
                print("[warning] get_id failed", url)

        return decorator

    return wrapper
