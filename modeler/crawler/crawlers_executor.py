from .models import Data
from crawler.crawlers.sdelanounas import collect_urls

#Proxy
#setup_proxy()

#CollectUrls('http://www.sdelanounas.ru', 'http://www.sdelanounas.ru/sphinxsearch/?s=росэнергоатом&page=')

def sdelanounas(url):
    print("sdelanounas()")
    collect_urls(url, 'http://www.sdelanounas.ru/sphinxsearch/?s=росэнергоатом&page=')

def contains_url(search_url):
    return Data.objects.filter(url=search_url).exists()

def save_content(url, content, date, tags):
    try:
        data = Data(url = url, content = content, date = date, tags = tags)
        data.save()
    except Exception as e:
        print('Исключение при записи в БД', url, e)