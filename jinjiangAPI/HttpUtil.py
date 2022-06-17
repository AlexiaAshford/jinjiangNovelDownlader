import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 5.1; Lenovo) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
                  "Chrome/39.0.0.0 Mobile Safari/537.36/JINJIANG-Android/206(Lenovo;android 5.1;Scale/2.0)",
    "Referer": "http://android.jjwxc.net?v=206"
}


def get_api(url: str, params: dict = None, return_type: str = "json"):
    if return_type == "json":
        return requests.get(url, params=params, headers=headers).json()
    elif return_type == "text":
        return requests.get(url, params=params, headers=headers).text
    elif return_type == "content":
        return requests.get(url, params=params, headers=headers).content


def post_api(url: str, data: dict = None, return_type: str = "json"):
    if return_type == "json":
        return requests.post(url, data=data, headers=headers).json()
    elif return_type == "text":
        return requests.post(url, data=data, headers=headers).text
    elif return_type == "content":
        return requests.post(url, data=data, headers=headers).content
