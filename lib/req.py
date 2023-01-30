import requests
from functools import wraps

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 5.1; Lenovo) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
                  "Chrome/39.0.0.0 Mobile Safari/537.36/JINJIANG-Android/206(Lenovo;android 5.1;Scale/2.0)",
    "Referer": "http://android.jjwxc.net?v=206"
}


def request(method, host, path):
    @wraps(request)
    def decorator(func):
        def wrapper(params):
            response = requests.request(method=method, url=host + path, params=params, headers=headers)
            try:
                return func(response.json())
            except Exception as e:
                print("request failed:", e, "url:", response.url, "\tres:", response.text)

        return wrapper

    return decorator
