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


class CheckJson:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        json, url = self.func(*args, **kwargs)
        if json.get("message"):
            print("message:", json.get("message"), "\t\turl:", url)
            return
        return json


class CheckJsonAndAddModel:
    def __init__(self, models=None):
        self.models = models

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            json, url = func(*args, **kwargs)
            if json.get("message"):
                return print("message:", json.get("message"), "\t\turl:", url)
            if self.models:
                return self.models(**json)
            return json

        return wrapper


@CheckJson
def get_json():
    return {"message": "errofegergrgr"}

# if __name__ == '__main__':
#     print(get_json())
# def check_json(func):
#     def wrapper(*args, **kwargs):
#         json = func(*args, **kwargs)
#         if json.get("message"):
#             print(json.get("message"))
#             return
#         return json
#
#     return wrapper
