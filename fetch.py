import time
import requests
import aiohttp
import asyncio

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed

async def fetch(session, url):
    async with session.get(url) as response:
        result = await response.text()
        return result

async def get_all(calls):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for call in calls:
            task = asyncio.ensure_future(fetch(
                session=session, 
                url=call))
            tasks.append(task)
            responses = asyncio.gather(*tasks)
            await responses

# use a semaphore

@timeit
def make_async_calls(calls):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(asyncio.ensure_future(get_all(calls)))
    print(result)

@timeit
def make_sync_calls(calls):
    for call in calls:
        result = requests.get(call)

if __name__ == '__main__':
    calls = ['https://python.org'] * 20
    make_async_calls(calls)
    make_sync_calls(calls)
