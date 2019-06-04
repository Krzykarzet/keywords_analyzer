import re
from contextlib import closing

from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException
import logging

logger = logging.getLogger(__name__)


def simple_get(url):
    """Get website"""
    result = None
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                result = resp.content
    except RequestException as e:
        log_error(e)

    return result


def is_good_response(resp):
    """Check if response is in correct format and is ok"""
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    logger.error(e)


def add_prefix(url):
    """check if url has http or https prefix and returns full url"""
    if url[0:7].lower() != "http://" and url[0:8].lower() != "https://":
        url = f"http://{url}"
    return url


def find_keywords(content):
    """Find """
    ret_val = ""
    soup = BeautifulSoup(content, 'html.parser')

    for tag in soup.find_all("meta"):
        name = tag.get("name", None)
        if name and name.lower() == "keywords":
        # if tag.get("name", None) in ["keywords", "Keywords", "KEYWORDS"]:
            ret_val += tag.get("content", None)

    return ret_val


def get_all_text(content):
    """Get all text from website"""
    soup = BeautifulSoup(content, 'html.parser')
    return soup.text


def find_words(content):
    """Search for text in paragraphs """
    soup = BeautifulSoup(content, 'html.parser')
    text_p = (''.join(s.findAll(text=True))for s in soup.findAll('p'))

    return text_p


def clean_wordlist(w_list):
    """Removing special characters and returns list"""
    clean_w_list = []

    for word in w_list:
        # Regex for latin leters and extra polish letters
        w = "".join(re.findall("[a-zA-ZżźćńółęąśŻŹĆĄŚĘŁÓŃ]+", word))
        if len(w) > 0:
            clean_w_list.append(w)

    return clean_w_list


def create_words_dict(words_list):
    """Creating dict word - count and returns dict"""
    word_count = {}

    for w in words_list:
        if w in word_count:
            word_count[w] += 1
        else:
            word_count[w] = 1

    return word_count


def find_keywords_in_words(keywords, words):
    """Finding keywords in all words dict and returns dict"""
    output = {}

    for kw in keywords:
        output[kw] = words[kw] if kw in words else 0

    # for kw in keywords:
    #     if kw in words:
    #         output[kw] = words[kw]
    #     else:
    #         output[kw] = 0

    return output

