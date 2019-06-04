from typing import List

from django.shortcuts import render
from django.views.decorators.http import require_POST

from . import engine


def index(request):
    return render(request, 'ka/index.html')


@require_POST
def results(request):
    url = engine.add_prefix(request.POST["website_url"])
    context = {'errors': 'wrong website'}
    content = engine.simple_get(url)

    if content:
        keywords = engine.find_keywords(content)
        keywords_list = keywords.split(",")

        raw_words = engine.find_words(content)
        words_list = []

        for w in raw_words:
            word = w.lower().split()
            word = engine.clean_wordlist(word)
            if len(word) > 0:
                words_list.append(word)

        words_list = [w for wl in words_list for w in wl]

        words_dict = engine.create_words_dict(words_list)

        keywords_count = engine.find_keywords_in_words(keywords_list, words_dict)

        context = {'keywords_list': keywords_list, 'keywords_count': keywords_count, 'url': url}

    return render(request, 'ka/results.html', context)
