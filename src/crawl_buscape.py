from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from cytoolz import *
from concurrent.futures import ThreadPoolExecutor


if __name__ == '__main__':
    caps = webdriver.DesiredCapabilities().FIREFOX
    caps['marionette'] = False
    d = webdriver.Firefox(capabilities=caps)
    base_url = 'http://www.buscape.com.br/xprocura?kw=&eid={}&pagina={}'
