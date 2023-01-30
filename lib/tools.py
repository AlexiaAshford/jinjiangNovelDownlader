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


# 使用类装饰器检测dict数据是否存在message字段

class CheckJson:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        json = self.func(*args, **kwargs)
        if json.get("message"):
            print(json.get("message"))
            return
        return json


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
