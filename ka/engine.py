from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import builtwith
import urllib3
import re


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


def get_all_text(content):
    soup = BeautifulSoup(content, 'html.parser')
    return soup.text


def find_words(content):
    soup = BeautifulSoup(content, 'html.parser')
    text_p = (''.join(s.findAll(text=True))for s in soup.findAll('p'))

    return text_p


def clean_wordlist(w_list):
    clean_w_list = []

    for word in w_list:
        w = "".join(re.findall("[a-zA-ZżźćńółęąśŻŹĆĄŚĘŁÓŃ]+", word))
        if len(w) > 0:
            clean_w_list.append(w)

    return clean_w_list


def create_words_dict(words_list):
    word_count = {}

    for w in words_list:
        if w in word_count:
            word_count[w] += 1
        else:
            word_count[w] = 1

    return word_count
