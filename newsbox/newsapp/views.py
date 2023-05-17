from django.shortcuts import render
from django.core.paginator import Paginator
import pysolr
from .constants import SOLR_URL

# Create your views here.
def index(request):
    solr = pysolr.Solr(SOLR_URL)
    results = solr.search('*:*', **{'rows': 200})
    news = []
    for result in results:
        title = result['title']
        description = result['description']
        url = result['url']
        imageurl = result.get('imageURL', 'nill')
        id = result['id']
        publishedat = result['publishedAt']
        author = result.get('author', 'nill')
        category = result['category']
        news.append((title, description, url, id, publishedat, category, imageurl, author))

    paginator = Paginator(news, 30)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    return render(request, 'newsapp/index.html', {'page': page})

def category(request):
    getcategory = request.GET.get('category')
    solr = pysolr.Solr(SOLR_URL)
    query = f'category:{getcategory}'
    results = solr.search(query, **{'rows': 100})
    news = []
    for result in results:
        title = result['title']
        description = result['description']
        url = result['url']
        imageurl = result.get('imageURL', 'nill')
        id = result['id']
        publishedat = result['publishedAt']
        author = result.get('author', 'nill')
        category = result['category']
        news.append((title, description, url, id, publishedat, category, imageurl, author))

    return render(request, 'newsapp/category.html', {'news': news, 'selected_category': getcategory})

def search(request):
    query = request.GET.get('query')
    solr = pysolr.Solr(SOLR_URL)
    results = solr.search(q='title:' + query, fq='title:' + query, **{'rows': 20})
    news = []
    for result in results:
        title = result['title']
        description = result['description']
        url = result['url']
        imageurl = result.get('imageURL', 'nill')
        id = result['id']
        publishedat = result['publishedAt']
        author = result.get('author', 'nill')
        category = result['category']
        news.append((title, description, url, id, publishedat, category, imageurl, author))

    return render(request, 'newsapp/search.html', {'news': news, 'query': query})