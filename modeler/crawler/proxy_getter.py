from bs4 import BeautifulSoup
import requests
import random
import time
import os

def get_html_proxy(url):
	r = requests.get(url)
	return r.text

def get_viable_proxy_list(html, wanted_num):
	soup = BeautifulSoup(html,'lxml')
	proxies = soup.find('tbody').find_all('tr')
	list_of_viable_proxies = []
	# Список сайтов для проверки прокси
	site_check_list = ['http://google.ru',
						'http://yandex.ru',
						'http://facebook.com',
						'http://yahoo.com',
						'http://wikipedia.org']
	for proxy in proxies[:wanted_num]:
		data = proxy.find('td').find('a').get_text()
		# Попытка перехода на сайты для проверки прокси.
		try:
			i = 0
			r = requests.get(site_check_list[i], timeout = None, proxies = {'': data})
			# 2xx все хорошо
			if r.status_code == 200:
				print(data)
				print(site_check_list[i],' Code = ',r.status_code)
				k = 'http://' + data
				list_of_viable_proxies.append(k)
			# 4xx ошибки клиента, 5xx ошибки сервера
			elif r.status_code in range(400, 452) or r.status_code in range(500,527) :
				i += 1
				r = requests.get(site_check_list[i], timeout = None, proxies = {'': data})
				print(data)
				print(site_check_list[i],' Code = ',r.status_code)
				k = 'http://' + data
				list_of_viable_proxies.append(k)
			else:
				print(data)
				print(r.status_code)
		except requests.exceptions.ConnectionError:
			print('Oops. Seems connection error!')
			continue
		except requests.exceptions.ConnectTimeout:
			print('Oops. Connection timeout occured!')
			continue 	
	print("Number of all proxies = ", len(proxies))
	print("Number of viable proxies = ", len(list_of_viable_proxies),'\n')

	# Проверка наличия прокси в списке.
	if len(list_of_viable_proxies) < 5:
		print('Найдено ',len(list_of_viable_proxies),' прокси')
		raise SystemExit(1)
	else:
		return list_of_viable_proxies


list_of_viable_proxies = get_viable_proxy_list(get_html_proxy('https://www.ip-adress.com/proxy-list'),10)
cur_dir = os.path.dirname(__file__)
useragent_filename = os.path.join(cur_dir, 'useragents.txt')
list_of_user_agents = open(useragent_filename).read().split('\n')
	

def get_html_with_proxy(url):
	time.sleep(round(abs(random.gauss(1.5, 1) + random.random()/10 + random.random()/100), 4))
	useragent = {'User-Agent': random.choice(list_of_user_agents)}
	proxy = {'http': random.choice(list_of_viable_proxies)}
	r = requests.get(url, timeout = None, headers = useragent, proxies = {'': proxy})
	return r.text

def main():
	url = 'https://www.ip-adress.com/proxy-list'	
	print("Full list of viable proxies = ",  get_viable_proxy_list(get_html_proxy(url), 20))

if __name__ == '__main__':
	main()