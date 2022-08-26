import requests
from . import UrlConstant
from tenacity import *

headers = {"User-Agent": UrlConstant.USER_AGENT_HEADER, "Referer": UrlConstant.REFERER_HEADER}


@retry(stop=stop_after_attempt(7), wait=wait_fixed(0.1))
def get(url: str, method: str = "GET", params: dict = None, re_type: str = "json") -> [dict, str, bytes]:
    api_url = UrlConstant.WEB_HOST + url.replace(UrlConstant.WEB_HOST, "")  # add web host
    if method == "GET":
        response = requests.request(method=method, url=api_url, params=params, headers=headers)
    else:
        response = requests.request(url=api_url, method=method, data=params, headers=headers)

    if re_type == "json" or re_type == "dict":
        return response.json()
    elif re_type == "text" or re_type == "str":
        return response.text
    elif re_type == "content" or re_type == "bytes":
        return response.content
    return response  # return request.response

