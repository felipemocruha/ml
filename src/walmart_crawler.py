from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from cytoolz import *
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from queue import Queue


def get_domain(url):
    return urlparse(url).netloc


def get_domain_links(domain, links):
    return [a.get('href') for a in links if urlparse(a.get('href')).netloc == domain]


def get_product_links(links):
    a = [url for url in links if url[-3:] == '/pr']
    print(a)
    return a


def crawl_one(driver, url, targets_queue, visited):
    visited.append(url)
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    WebDriverWait(driver, 2000)
    soup = BeautifulSoup(driver.page_source, 'html5lib')
    for l in get_product_links(get_domain_links('www.walmart.com.br', soup.find_all('a'))):
        if l not in visited:
            targets_queue.put_nowait(l)


if __name__ == '__main__':
    visited = []
    targets_queue = Queue()
    caps = webdriver.DesiredCapabilities().FIREFOX
    caps['marionette'] = False
    d = webdriver.Firefox(capabilities=caps)
    #d = webdriver.PhantomJS(executable_path='../node_modules/phantomjs/bin/phantomjs')

    with open('../data/walmart/crawler_seeds.txt') as f:
        targets = [url[:-1] for url in f.readlines()]
    crawl_one(d, targets[1], targets_queue, visited)
