import asyncio
import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from fetch import fetch
from parser import parse_page
from urllib.parse import urlparse
from cytoolz import *


ROOT_DIR = os.path.dirname(os.path.abspath('.'))
error_pages = []


def len_parsed(domain):
    with open('../data/{}/parsed_data.json'.format(domain),'r') as f:
        return (domain, len(json.loads(f.read())['products']))


def is_domain(domain, url):
    return urlparse(url).netloc == domain


def get_domain_urls(domain, seed):
    return list(filter(partial(is_domain, domain), seed))


def extract_domain_name(domain):
    return domain[4:-7]


def write_domain_links(file_name, links):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'w') as f:
        f.writelines(links)


def write_results(payload, domain):
    result = os.path.join(ROOT_DIR, 'data', domain, 'parsed_data.json')
    with open(result, 'w') as f:
        f.writelines(json.dumps(payload))


async def fetch_and_parse(url, data):
    try:
        page = await fetch(url)
        if page:
            data.append(parse_page(page))
    except Exception as err:
        error_pages.append(url)
        print('Error: {}\nURL: {}\n'.format(err, url))


async def worker(targets, data, counter):
    tasks = asyncio.as_completed([fetch_and_parse(url, data) for url in targets])
    domain = extract_domain_name(urlparse(targets[0]).netloc)

    for task in tasks:
        await task


def main(pair):
    domain, targets = pair
    data = []
    policy = asyncio.get_event_loop_policy()
    policy.set_event_loop(policy.new_event_loop())
    loop = asyncio.get_event_loop()
    counter = 0

    print('[*] Fetching and Parsing targets for {} ...'.format(domain))
    loop.run_until_complete(worker(targets, data, counter))

    payload = {'products': data}
    print('[*] Writing results...')
    write_results(payload, extract_domain_name(domain))

    print('[*] New data is available for {}!'.format(domain))


if __name__ == '__main__':
    with open(os.path.join(ROOT_DIR, 'data', 'targets.txt'), 'r') as f:
        all_urls = set([url[:-1] for url in f.readlines()])

    all_domains = set([urlparse(url).netloc for url in all_urls])

    domain_filter1 = ['www.americanas.com.br', 'www.shoptime.com.br',
                      'www.submarino.com.br']

    domain_filter2 = ['www.casasbahia.com.br','www.extra.com.br',
                      'www.pontofrio.com.br', 'www.walmart.com.br',
                      'www.magazineluiza.com.br']

    #domain_filter = domain_filter1 + domain_filter2
    domain_filter = ['www.walmart.com.br']

    domains = [extract_domain_name(url) for url in domain_filter]
    links = [(domain, get_domain_urls(domain, all_urls)) for domain in domain_filter]


    # execute main for each shop
    with ThreadPoolExecutor(max_workers=4) as ex:
        tasks = as_completed([ex.submit(main, pair) for pair in links])

    with open('../data/error_urls', 'w') as f:
        f.writelines(error_pages)

    print('[*] Results:')
    print([len_parsed(domain) for domain in domains])

    # # write links in separate files
    # for link in links:
    #     domain_name = extract_domain_name(link[0])
    #     file_name = os.path.join(ROOT_DIR, 'data', domain_name, '{}_urls'.format(domain_name))
    #     write_domain_links(file_name, link[1])
