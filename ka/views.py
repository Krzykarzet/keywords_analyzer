from django.shortcuts import render
from . import engine

# Create your views here.


def index(request):
    return render(request, 'ka/index.html')


def results(request):
    url = engine.add_prefix(request.POST["website_url"])
    if engine.simple_get(url):
        keywords = engine.find_keywords(engine.simple_get(url))
        keywords_list = ''.join(k for k in keywords)
        context = {'keywords_list': keywords_list}
    else:
        context = {'errors': 'wrong website'}

    return render(request, 'ka/results.html', context)
