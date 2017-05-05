import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from cytoolz import *
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from random import choice, randint
from bs4 import BeautifulSoup


UA_LIST = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36']


def make_product(desc, image, price):
    print('[*] Making one product...')
    return {'description': desc,
            'image': image,
            'price': price}


def extract_product_list(li):
    product_list = []
    for product in li:
        container = product.find('div', class_='image')
        p = container.find('img')
        desc = p.get('alt')
        image = p.get('src')
        price = container.find('a').get('data-preco')
        product_list.append(make_product(desc, image, price))
    return product_list


def fetch_one(url):
    print('[*] Fetching {}'.format(url))
    headers = {'User-Agent': choice(UA_LIST)}
    r = requests.get(url, headers=headers)
    if r.ok:
        print('[*] Request {} OK!'.format(url))
        soup = BeautifulSoup(r.text, 'html5lib')
        ul = soup.find('ul', class_='bp-product-list')
        li = ul.find_all('li', class_='product track_checkout_container offer')
        return extract_product_list(li)


def main(url, final):
    for result in fetch_one(url):
        final.append(result)


if __name__ == '__main__':
    base_url = 'http://www.buscape.com.br/xprocura?kw=&eid={}&pagina={}'
    eid = 125
    pages = set([base_url.format(eid, randint(1,24000)) for i in range(500)])

    final = []
    with ThreadPoolExecutor(max_workers=50) as ex:
        tasks = as_completed([ex.submit(main, url, final) for url in pages])

    products = list(concat([final]))
    print('[*] Writing results...')
    with open('../data/shoptime/buscape.json', 'w') as f:
        f.writelines(json.dumps({'products': products}))
    print('[*] New data is available!')
