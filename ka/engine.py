from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import builtwith
import urllib3


def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                ret_val = resp.content
            else:
                ret_val = None
    except RequestException as e:
        log_error(e)
        ret_val = None

    return ret_val


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    print(e)


def add_prefix(url):
    if url[0:7].lower() != "http://" and url[0:8].lower() != "https://":
        return "http://"+url
    else:
        return url


def find_keywords(content):
    ret_val = ""
    soup = BeautifulSoup(content, 'html.parser')

    for tag in soup.find_all("meta"):
        if tag.get("name", None) in ["keywords", "Keywords", "KEYWORDS"]:
            ret_val += tag.get("content", None)

    return ret_val
