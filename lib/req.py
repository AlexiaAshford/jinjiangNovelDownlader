import requests
from functools import wraps


def request(method, host, path):
    @wraps(request)
    def decorator(func):
        def wrapper(params):
            response = requests.request(method=method, url=host + path, params=params)

            return func(response.json())

        return wrapper

    return decorator
