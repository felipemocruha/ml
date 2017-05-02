#coding: utf-8
import re
import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from urllib.parse import urlparse
from unicodedata import normalize
from cytoolz import *

def tokenize_url(url):
    path = urlparse(url).path
    path = path.replace('/', ' ')
    path = path.replace('-', ' ')
    return word_tokenize(path)


def remove_accents(input_str):
    return normalize('NFKD', input_str).encode('ascii', 'ignore').decode()


def sanitize_string(input_str):
    pattern = r'[?|&|!|@|#|;|*|~|(|)|´|^|\r|\n|\t]'
    return clean_string(re.sub(pattern, r'', remove_accents(input_str.lower())))


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


def extract_title(soup):
    return soup.find('title').get_text().replace('\n', ' ')


def clean_string(input_str):
    input_str = input_str.replace('.', ' ').replace(',', ' ')

    unuseful = set(['confira', 'compre', 'oferta', 'novo',
                    'preco', 'agora', 'melhores', 'aqui',
                    'aproveite', 'menor', 'maior', 'encontra',
                    'site', 'condicoes', 'ofertas', 'imbativeis',
                    'vendas', 'online', 'novo', 'nova', 'tecnologia',
                    'precos', 'pagamento', 'melhor', 'veja', 'encontre',
                    'menores', 'vem', 'venha', 'ver'])

    names = set(['walmart', 'walmart.com', 'shoptime', 'shoptime.com',
                 'pontofrio', 'pontofrio.com', 'magazineluiza', 'magazineluiza.com',
                 'magazine luiza', 'americanas', 'americanas.com', 'submarino',
                 'submarino.com', 'extra', 'extra.com.br', 'casas bahia', 'casasbahia.com.br'])

    stopwords = [remove_accents(s) for s in nltk.corpus.stopwords.words('portuguese')]
    repl = list(concat([unuseful, names, stopwords]))
    tk = word_tokenize(input_str)
    return ' '.join([word for word in tk if word not in repl])


def parse_page(page):
    soup = get_soup(page)
    title = sanitize_string(extract_title(soup))
    meta = extract_meta(soup)
    meta.append({'title': title})
    table = extract_table(soup)
    payload = {}
    if meta:
        payload['meta'] = meta
    if table:
        payload['table'] = table
    return payload
