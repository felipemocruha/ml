import os
import json
import requests
from parser import parse_page


ROOT_DIR = os.path.dirname(os.path.abspath('.'))


def fetch(url):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}).text
    print('fetched one')
    return r


def load_targets():
    targets_file = os.path.join(ROOT_DIR, 'data', 'targets.txt')
    with open(targets_file, 'r') as f:
        targets = [url[:-1] for url in f.readlines()]
        return targets


def write_results(payload):
    result = os.path.join(ROOT_DIR, 'data', 'meta_results.json')
    with open(result, 'w') as f:
        f.writelines(json.dumps(payload))


def fetch_and_parse(target):
    page = fetch(target)
    return parse_page(page)


async def main(loop):
    print('[*] Loading targets.')
    targets = load_targets()
    print('[*] Fetching and Parsing targets.')
    data = [await fetch_and_parse(page) for page in targets]
    payload = {'products': data}
    write_results(payload)
    print('[*] Data is now available!')


if __name__ == '__main__':
    print('[*] Loading targets.')
    targets = load_targets()
    print('[*] Fetching and Parsing targets.')
    data = [fetch_and_parse(page) for page in targets]
    payload = {'products': data}
    write_results(payload)
    print('[*] Data is now available!')
