import requests


def request(url: str, method: str, params: dict):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1; Lenovo) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
                      "Chrome/39.0.0.0 Mobile Safari/537.36/JINJIANG-Android/206(Lenovo;android 5.1;Scale/2.0)",
        "Referer": "http://android.jjwxc.net?v=206"
    }
    if method == "GET":
        return requests.request(method=method, url=url, params=params, headers=headers)
    else:
        return requests.request(url=url, method=method, data=params, headers=headers)
