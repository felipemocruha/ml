import asyncio
import aiohttp
import requests
import async_timeout
import json
from random import choice, randint


UA_LIST = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36']


async def fetch(url):
    await asyncio.sleep(randint(1,5))
    headers = {'User-Agent': choice(UA_LIST)}
    with aiohttp.TCPConnector(limit_per_host=20) as conn:
        with async_timeout.timeout(60):
            async with aiohttp.request('GET', url,
                                       headers=headers, connector=conn) as response:
                return await response.text() if response.status == 200 else None


def fetch_sync(url):
    sleep(3)
    headers = {'User-Agent': choice(UA_LIST)}
    return requests.get(url, headers=headers).text
