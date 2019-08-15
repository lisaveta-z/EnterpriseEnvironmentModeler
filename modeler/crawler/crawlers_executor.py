from .models import Data
from .models import Resource
from crawler.crawlers.sdelanounas import sdelanounas_crawler
from crawler.crawlers.rosenergoatom import rosenergoatom_crawler
from crawler.crawlers.atomicenergy import atomicenergy_crawler
from crawler import proxy_getter
import re
import sys
import dateparser

def exec_crawler():
    print("exec_crawler")
    proxy_getter.setup_proxy()
    thismodule = sys.modules[__name__]
    resources = Resource.objects.all()
    for res in resources:
        #if (res.name == "sdelanounas") or (res.name == "rosenergoatom"):
        #    continue
        getattr(thismodule, res.name)(res.url)


def sdelanounas(url):
    print("sdelanounas()")
    sdelanounas_crawler(url, 'http://www.sdelanounas.ru/sphinxsearch/?s=росэнергоатом&page=')

def rosenergoatom(url):
    print("rosenergoatom()")
    rosenergoatom_crawler(url, 'http://www.rosenergoatom.ru/zhurnalistam/news-archive/')

def atomicenergy(url):
    print("atomicenergy()")
    atomicenergy_crawler(url)


def contains_url(search_url):
    return Data.objects.filter(url=search_url).exists()


def save_content(url, content, date, tags):
    try:
        data = Data(url = url, content = content, date = format_date(date), tags = tags)
        data.save()
    except Exception as e:
        print('Исключение при записи в БД', url, e)


def format_date(date_string):
    date_string = re.sub("\s\s+", " ", date_string.strip())
    if date_string == "":
        return None
    return dateparser.parse(date_string)