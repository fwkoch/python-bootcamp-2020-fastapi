import asyncio
import time

import aiohttp
import requests


async def fetch(session):
    resp = await session.get("https://github.com/fwkoch")
    print(resp.status)
    return resp.status


async def fetch_ten_times():
    session = aiohttp.ClientSession()
    tasks = await asyncio.gather(
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
    )
    await session.close()


# async def fetch_async(session):
#     resp = await session.get("https://github.com/fwkoch")
#     print(resp.status)
#     return resp.status


# async def fetch_async_ten_times():
#     session = aiohttp.ClientSession()
#     tasks = await asyncio.gather(
#         fetch_async(session),
#         fetch_async(session),
#         fetch_async(session),
#         fetch_async(session),
#         fetch_async(session),
#         fetch_async(session),
#         fetch_async(session),
#         fetch_async(session),
#         fetch_async(session),
#         fetch_async(session),
#     )
#     await session.close()


if __name__ == "__main__":
    start = time.time()
    asyncio.run(fetch_ten_times())
    print(f"Elapsed time: {time.time() - start}")

    # start = time.time()
    # asyncio.run(fetch_async_ten_times())
    # print(f"Elapsed time: {time.time() - start}")
