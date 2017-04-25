#coding: utf-8
import re
import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from urllib.parse import urlparse
from unicodedata import normalize


def tokenize_url(url):
    path = urlparse(url).path
    path = path.replace('/', ' ')
    path = path.replace('-', ' ')
    return word_tokenize(path)


def remove_accents(input_str):
    return normalize('NFKD', input_str).encode('ascii', 'ignore').decode()


def sanitize_string(input_str):
    pattern = r'[?|&|!|@|#|;|*|~|(|)|´|^]'
    input_str = re.sub(pattern, r'', remove_accents(input_str.lower()))
    return input_str


def match_keywords(meta):
    keywords = ['url', 'title', 'price', 'description', 'image', 'sku', 'brand']
    for k in keywords:
        match = re.search(k, meta.prettify().lower())
        if match:
            return meta


def get_soup(response):
    return BeautifulSoup(response, 'html.parser')


def extract_meta(soup):
    meta = soup.find_all('meta')
    filtered = [m for m in [match_keywords(m) for m in meta if match_keywords(m)] if m is not None]
    return [m for m in [process_meta(m) for m in filtered] if m is not None]


def process_meta(meta):
    values = list(meta.attrs.values())
    if len(values) > 1:
        return {sanitize_string(values[0]): sanitize_string(values[1])}


def extract_table(soup):
    product_info = {}
    for tr in soup.find_all('tr'):
        td = tr.find_all('td')
        if len(td) == 2:
            key = sanitize_string(td[0].getText())
            value = sanitize_string(td[1].getText())
            product_info[key] = value
    return product_info


def parse_page(page):
    soup = get_soup(page)
    meta = extract_meta(soup)
    table = extract_table(soup)
    payload = {}
    if meta:
        payload['meta'] = meta
    if table:
        payload['table'] = table
    return payload
