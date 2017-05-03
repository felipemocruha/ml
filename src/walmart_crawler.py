from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from cytoolz import *
from concurrent.futures import ThreadPoolExecutor


def crawl_one(url, targets_queue, visited):
    d.get(url)



if __name__ == '__main__':
    visited = []
    caps = webdriver.DesiredCapabilities().FIREFOX
    caps['marionette'] = False
    d = webdriver.Firefox(capabilities=caps)
    with open('../data/walmart_crawler_targets.txt') as f:
        targets = set([url[:-1] for url in f.readlines()])
