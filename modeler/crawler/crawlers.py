from .proxy_getter import get_viable_proxy_list
from .proxy_getter import get_html_proxy
from bs4 import BeautifulSoup
import requests
import random
import time
import os
from .models import Data

def Crawl(webUrl):
    url = webUrl
    html = getHtmlWithProxy(url)
    s = BeautifulSoup(html, "html.parser")
    f = open("crawlerResult.txt", mode='a', encoding='utf8')
    hasError = False

    #Дата статьи
    try:
        date = s.findAll('li', {'class':'time'})[0]
        if date.findAll('span'):
            date.span.replace_with(" ")
        date = date.text
    except Exception as e:
        print("Исключение при определении даты статьи", url, e)
        date = ""
        hasError = True
    dateText = "%s %s\n" % ("DATE:", date)

    #URL
    urlText = "%s %s\n" % ("URL:", webUrl)
    print(urlText)
    f.write(urlText) 

    #Заголовок статьи
    header = ""
    try:
        if s.findAll('h1', {'class':'h1_openblog'}):
            header = s.findAll('h1', {'class':'h1_openblog'})[0]
        else:
            header = s.findAll('h1', {'class':'unique'})[0]
        header = header.text.strip()
    except Exception as e:
        print("Исключение при определении заголовка статьи", url, e)
        header = ""
    headerText = "%s %s\n" % ("HEADER:", header)
    print(headerText)
    f.write(headerText) 

    #Содержимое статьи
    try:
        content = []
        article = s.findAll('div', {'class':'text __sun_article_text'})[0]
        if (article.text == '\n'):
            article = s.contents[4]
        else:
            while article.findAll('li'):
                article.li.replace_with("")
        while article.findAll('div'):
            article.div.replace_with("")
        content.append("" if article.text is None else article.text.replace("\n", ""))
        content = "".join(content)
    except Exception as e:
        print("Исключение при определении содержимого статьи", url, e)
        content = ""
        hasError = True
    contentText = "%s %s\n" % ("CONTENT:", content)
    print(contentText)
    f.write(contentText) 

    #Дата статьи
    print(dateText)
    f.write(dateText) 

    #Теги
    tags = []
    try:
        for tag in s.findAll('a', {'class':'article-tag'}):
            tags.append(tag.text)
    except Exception as e:
        print("Исключение при определении тегов статьи", url, e)
        tags = []
        hasError = True
    tags = ", ".join(tags)
    tagsText = "%s %s\n" % ("TAGS:", tags)
    print(tagsText)
    f.write(tagsText) 

    #Разделитель для печати в файл и на консоль
    separatorText = "__________________________________________________________________________________\n"
    print(separatorText)
    f.write(separatorText)

    f.close()

    # Обращение к внешнему объекту elasticsearchCrawlerClient
    #try:
    #    if not(elasticsearchCrawlerClient.contains(url)) and not(hasError):
    #        elasticsearchCrawlerClient.put(url, content, date, tags)
    #except Exception as e:
    #    print('Исключение при записи в БД', e)

    # Обращение к database
    try:
        if not(hasError):
            data = Data(url = url, content = content, date = date, tags = tags)
            data.save()
    except Exception as e:
        print('Исключение при записи в БД', e)


def CollectUrls(baseUrl, searchUrl):
    f = open("crawlerResult.txt", "w+")
    f.close()
    flag = True
    count = 0

    #Обходим все ссылки в поиске по сайту по "Росэнергоатом"
    while(flag):
        try:
            flag = False
            url = "%s%s" % (searchUrl, count)
            html = getHtmlWithProxy(url)
            s = BeautifulSoup(html, "html.parser")
            count += 1

            for heading in s.findAll('div', {'class':'heading'}):
                flag = True
                search_url = "%s%s" % (baseUrl, heading.h4.a.get('href'))
                if not(contains_url(search_url)):
                    Crawl(search_url)
                #Crawl("%s%s" % ('http://www.sdelanounas.ru', '/blogs/5307'))
        except Exception as e:
            print('Исключение в CollectUrls', e)
            continue

def getHtmlWithProxy(url):
    time.sleep(round(abs(random.gauss(1.5, 1) + random.random()/10 + random.random()/100), 4))
    useragent = {'User-Agent': random.choice(list_of_user_agents)}
    proxy = {'http': random.choice(list_of_viable_proxies)}
    r = requests.get(url, timeout = None, headers = useragent, proxies = {'': proxy})
    return r.text


#Proxy
list_of_viable_proxies = get_viable_proxy_list(get_html_proxy('https://www.ip-adress.com/proxy-list'),10)
cur_dir = os.path.dirname(__file__)
useragent_filename = os.path.join(cur_dir, 'useragents.txt')
list_of_user_agents = open(useragent_filename).read().split('\n')

#CollectUrls('http://www.sdelanounas.ru', 'http://www.sdelanounas.ru/sphinxsearch/?s=росэнергоатом&page=')

def sdelanounas(url):
    print("sdelanounas()")
    CollectUrls(url, 'http://www.sdelanounas.ru/sphinxsearch/?s=росэнергоатом&page=')

def contains_url(search_url):
    return Data.objects.filter(url=search_url).exists()