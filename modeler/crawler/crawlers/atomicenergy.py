from crawler import crawlers_executor
from crawler.proxy_getter import get_html_with_proxy
from bs4 import BeautifulSoup
import requests
import random
import time
import os
import re

def atomicenergy_crawler(main_url):
    # Получаем ссылки с главной страницы
    text = get_html_with_proxy(main_url)
    soup = BeautifulSoup(text, "html.parser")
    li = soup.find('nav').find('ul').find_all('li')
    urls = []
    for i in li:
        href = i.find('a', href = True)['href']
        if 'www' in href or ':' in href:
            continue
        href = main_url + href
        if href not in urls:
            urls.append(href)
    print(urls)
    # записываем все возможные ссылки
    for u in urls:
        _text = get_html_with_proxy(u)
        _soup = BeautifulSoup(_text, "html.parser")
        
        # находим ссылку
        for a in _soup.find_all('a'):
            if 'www' in a or ':' in a or 'http' in a:
                continue
            check = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',a['href'])
            if len(check) > 0:
                continue
            link = main_url + a['href']

            if (link not in urls) and not(crawlers_executor.contains_url(link)):
                _text_ = get_html_with_proxy(link)
                _soup_ = BeautifulSoup(_text_, "html.parser")
                crawl(link, _soup_)
                urls.append(link)


def crawl(link, soup):
    
    # Заголовок
    try:
        title = soup.find('div', {'class':'clearfix'}).find('h1').text
    except Exception as e:
        print("Исключение при определении заголовка статьи", url, e)
        title = ""
    titleText = "%s %s\n" % ("TITLE:", title)
    print(titleText)
    
    # Данные
    ps = soup.find_all('p')
    data = ""
    try:
        for p in ps:
            data += p.text + '\n'
    except Exception as e:
        print("Исключение при определении содержимого статьи", url, e)
        data = ""
    dataText = "%s %s\n" % ("CONTENT:", data)
    print(dataText)
    
    # Дата
    date = ""
    try:
        date = ''.join([c if c not in ['\n','\t'] else '' for c in soup.find('div', {'class': 'node-meta__date'}).text])
    except Exception as e:
        print("Исключение при определении даты статьи", url, e)
        date = ""
    dateText = "%s %s\n" % ("DATE:", date)
    print(dateText)
    
    # Тэги
    try:
        tags = soup.find('div', {'class': 'block-atom-sidebar-taxonomy block block-atom-sidebar clearfix'})
        content = tags.find('div', {'class': 'content'}).find_all('div', class_="title")
        t = []
        for tag in content:
            te = tag.find('a').text
            sp = tag.find('span').text
            t.append(te.strip()) #te + sp + ' '
    except Exception as e:
        print("Исключение при определении тегов статьи", url, e)
        t = []
    tags = ", ".join(t)
    tagsText = "%s %s\n" % ("TAGS:", tags)
    print(tagsText)

    print(''.join(['-' for i in range(50)]) + '\n')

    # Запись в БД
    crawlers_executor.save_content(link, data, date, tags, title)   
    

if __name__ == "__main__":
    atomicenergy_crawler()
