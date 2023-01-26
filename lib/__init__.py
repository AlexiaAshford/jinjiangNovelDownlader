import re

import requests
from functools import wraps, partial


def request(method, host, path):
    @wraps(request)
    def decorator(func):
        def wrapper(params):
            response = requests.request(method=method, url=host + path, params=params)

            return func(response.json())

        return wrapper

    return decorator


def get_url_id():
    def wrapper(func):
        def decorator(url: str):
            result = re.compile(r'(\d+)').findall(str(url))
            if len(result) > 0 and str(result[0]).isdigit():
                func(result[0])
            else:
                print("[warning] get_id failed", url)

        return decorator

    return wrapper


GET = partial(request, "GET", "https://app-cdn.jjwxc.net/androidapi/")
POST = partial(request, "POST", "https://app-cdn.jjwxc.net/androidapi/")
