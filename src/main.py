import asyncio
import os
import json
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from fetch import fetch
from parser import parse_page


ROOT_DIR = os.path.dirname(os.path.abspath('.'))


def load_targets():
    targets_file = os.path.join(ROOT_DIR, 'data', 'targets.txt')
    with open(targets_file, 'r') as f:
        targets = [url[:-1] for url in f.readlines()]
        return targets


def write_results(payload):
    result = os.path.join(ROOT_DIR, 'data', 'meta_results.json')
    with open(result, 'w') as f:
        f.writelines(json.dumps(payload))


async def fetch_and_parse(url, data):
    try:
        page = await fetch(url)
        data.append(parse_page(page))
    except Exception as err:
        print('Error: {}\nURL: {}\n'.format(err, url))


async def worker(targets, data, counter):
    tasks = [fetch_and_parse(url, data) for url in targets]
    tasks_it = asyncio.as_completed(tasks)

    for task in tasks_it:
        await task
        print('Task {} done!'.format(counter))
        counter += 1


if __name__ == '__main__':
    data = []
    loop = asyncio.get_event_loop()
    counter = 0

    print('[*] Loading targets...')
    targets = load_targets()

    print('[*] Fetching and Parsing targets...')
    loop.run_until_complete(worker(targets, data, counter))

    payload = {'products': data}
    print('[*] Writing results...')
    write_results(payload)

    print('[*] New data is available...')
