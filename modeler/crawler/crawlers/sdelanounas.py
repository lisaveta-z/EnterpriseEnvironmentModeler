from crawler.crawlers_executor import contains_url
from crawler.proxy_getter import get_html_with_proxy
from bs4 import BeautifulSoup
import requests
import random
import time
import os

#Функция парсинга html-страницы, представляющей собой статью
def crawl(url):
    html = get_html_with_proxy(url)
    s = BeautifulSoup(html, "html.parser")

    #Дата статьи
    try:
        date = s.findAll('li', {'class':'time'})[0]
        if date.findAll('span'):
            date.span.replace_with(" ")
        date = date.text
    except Exception as e:
        print("Исключение при определении даты статьи", url, e)
        date = ""
    dateText = "%s %s\n" % ("DATE:", date)
    print(dateText)

    #URL
    urlText = "%s %s\n" % ("URL:", url)
    print(urlText)

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
    contentText = "%s %s\n" % ("CONTENT:", content)
    print(contentText)

    #Теги
    tags = []
    try:
        for tag in s.findAll('a', {'class':'article-tag'}):
            tags.append(tag.text)
    except Exception as e:
        print("Исключение при определении тегов статьи", url, e)
        tags = []
    tags = ", ".join(tags)
    tagsText = "%s %s\n" % ("TAGS:", tags)
    print(tagsText)

    #Разделитель для печати на консоль
    print("__________________________________________________________________________________\n")

    # Запись в БД
    save_content()


#Функция сбора ссылок на статьи и запуск парсинга каждой статьи в цикле, если ее нет в БД
def collect_urls(base_url, search_url):
    flag = True
    count = 0

    #Обходим все ссылки в поиске по сайту по "Росэнергоатом"
    while(flag):
        try:
            flag = False
            url = "%s%s" % (search_url, count)
            html = get_html_with_proxy(url)
            s = BeautifulSoup(html, "html.parser")
            count += 1

            for heading in s.findAll('div', {'class':'heading'}):
                flag = True
                article_url = "%s%s" % (base_url, heading.h4.a.get('href'))
                if not(contains_url(article_url)):
                    crawl(article_url) #crawl("%s%s" % ('http://www.sdelanounas.ru', '/blogs/5307'))
        except Exception as e:
            print('Исключение в collect_urls()', e)
            continue

