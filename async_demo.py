import asyncio
import time

import aiohttp
import requests


def fetch(session):
    resp = session.get("https://github.com/fwkoch")
    print(resp.status_code)
    return resp.status_code


def fetch_ten_times():
    session = requests.Session()
    tasks = [
        fetch(session),
        fetch(session),
        fetch(session),
        fetch(session),
        fetch(session),
        fetch(session),
        fetch(session),
        fetch(session),
        fetch(session),
        fetch(session),
    ]
    session.close()


async def fetch_async(session):
    resp = await session.get("https://github.com/fwkoch")
    print(resp.status)
    return resp.status


async def fetch_async_ten_times():
    session = aiohttp.ClientSession()
    tasks = await asyncio.gather(
        fetch_async(session),
        fetch_async(session),
        fetch_async(session),
        fetch_async(session),
        fetch_async(session),
        fetch_async(session),
        fetch_async(session),
        fetch_async(session),
        fetch_async(session),
        fetch_async(session),
    )
    await session.close()


if __name__ == "__main__":
    start = time.time()
    fetch_ten_times()
    print(f"Elapsed time: {time.time() - start}")

    start = time.time()
    asyncio.run(fetch_async_ten_times())
    print(f"Elapsed time: {time.time() - start}")
