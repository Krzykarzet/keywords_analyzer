from typing import List
from .classes import Website
from django.shortcuts import render
from . import engine as e
from django.views.decorators.http import require_POST


def index(request):
    return render(request, 'ka/index.html')


@require_POST
def results(request):
    url = e.add_prefix(request.POST["website_url"])
    if e.simple_get(url):
        content = e.simple_get(url)
        keywords = e.find_keywords(content)
        keywords_list = keywords.split(",")

        raw_words = e.find_words(content)
        words_list: List[List[str]] = []

        for w in raw_words:
            word = w.lower().split()
            word = e.clean_wordlist(word)
            if len(word) > 0:
                words_list.append(word)

        words_list = [w for wl in words_list for w in wl]

        words_dict = e.create_words_dict(words_list)

        keywords_count = e.find_keywords_in_words(keywords_list, words_dict)

        context = {'keywords_list': keywords_list, 'keywords_count': keywords_count, 'url': url}
    else:
        context = {'errors': 'wrong website'}

    # all_text = e.get_all_text(e.simple_get(url))

    # context = {**context,  **{'text': all_text}}

    return render(request, 'ka/results.html', context)


@require_POST
def cresults(request):
    context = {}

    w = Website(request.POST["website_url2"])


    return render(request, 'ka/cresults.html', context)
