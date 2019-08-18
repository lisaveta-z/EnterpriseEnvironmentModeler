from crawler import crawlers_executor
from crawler.proxy_getter import get_html_with_proxy
import requests
import time
import random
import os
from bs4 import BeautifulSoup

# Подсчет кол-ва статей
numberArticle = 0

def rosenergoatom_crawler(url, old_url):
    # Статьи за 2017-2018
    new_article_url(url)

    # Статьи за 2010-2016
    year = 2010
    while (year <= 2016):
        year_url = str(year) + '/'
        old_article_url("%s%s" % (old_url, year_url))
        year += 1


def new_article_url(start_url):
    web_url = "%s%s" % (start_url, '29278?PAGEN_1=')
    count = 7
    global numberArticle

    while (count >= 0):
        page_url = "%s%s" % (web_url, count)
        code = get_html_with_proxy(page_url)
        s = BeautifulSoup(code, "html.parser")
        count -= 1

        for a in s.findAll('p', {'class':'news-item'}):
            #print("NUMBER OF ARTICLE: ", numberArticle, '\n')
            item_id = a.get('id')
            length = len(item_id)
            item_start = item_id.rfind('_', 0, length) + 1
            item = item_id[item_start:length:1] + '/'
            article_url = "%s%s" % (start_url, item)
            if not(crawlers_executor.contains_url(article_url)):
                crawl(article_url)
            numberArticle += 1


def old_article_url(start_url):
    web_url = "%s%s" % (start_url, '?PAGEN_1=')
    count = 0
    global numberArticle

    # Определение кол-ва страниц
    url_pages = "%s%s" % (web_url, 0)
    code_pages = get_html_with_proxy(url_pages)
    soup_page = BeautifulSoup(code_pages, "html.parser")
    pages = soup_page.find('a',{'class':'modern-page-dots'}).find_next_sibling('a')

    while (count <= int(pages.text)):
        page_url = "%s%s" % (web_url, count)
        code = get_html_with_proxy(page_url)
        s = BeautifulSoup(code, "html.parser")
        count += 1
        head = s.findAll('div', {'class':'news-list'})[2]

        for a in head.findAll('p', {'class':'news-item'}):
            #print("NUMBER OF ARTICLE: ", numberArticle, '\n')
            item_id = a.get('id')
            length = len(item_id)
            item_start = item_id.rfind('_', 0, length) + 1
            item = 'index.php?ELEMENT_ID=' + item_id[item_start:length:1]
            article_url = "%s%s" % (start_url, item)
            if not(crawlers_executor.contains_url(article_url)):
                crawl(article_url)
            numberArticle += 1


def crawl(url):
    code = get_html_with_proxy(url)
    soup = BeautifulSoup(code, "html.parser")
    print(url)

    #Дата
    try:
        div = soup.find('div', {'id': 'content'})
        date = div.find('span', {'class': 'news-date-time'})
        date = date.text        
    except Exception as e:
        print("Исключение при определении даты статьи", url, e)
        date = ""
    dateText = "\n%s %s\n" % ("DATE:", date)
    print(dateText)

    #Tag
    # tag = soup.find('div', {'class':'col-lg-6 content-block'}).find('h1')
    try:
        tag = div.find('small', {'class': 'sourcetext'})
        tag = tag.text.strip()      
    except Exception as e:
        print("Исключение при определении тегов статьи", url, e)
        tags = ""
    tagText = "%s %s\n" % ("TAG:", tag)
    print(tagText)

    #Заголовок
    try:
        title = div.find('p', {'class': 'detnewsTitle'})
        title = title.text.strip()
    except Exception as e:
        print("Исключение при определении заголовка статьи", url, e)
        title = ""
    titleText = "%s %s\n" % ("TITLE:", title)
    print(titleText)

    #Статья
    try:
        content = div.find('div').find('div')
        content = content.text.strip().replace("\n", "")
    except Exception as e:
        print("Исключение при определении содержимого статьи", url, e)
        content = ""
    contentText = "%s %s\n" % ("CONTENT:", content)
    print(contentText)

    #Разделитель
    separatorText = "______________________________________________________________________________________\n"
    print(separatorText)

    # Запись в БД
    crawlers_executor.save_content(url, content, date, tag, title)
