"""This modules contains functions to handle asynchronous
http requests"""
import asyncio
import aiohttp

payload = {'id': '2829', 'holdthedoor': 'Enviar'}

async def makepost_req(url, session):
    async with session.post(url, data=payload) as res:
        if len(await res.text()) > 100:
            return 1
        return 0


def get_tasks(url, session, total_req=1):
    """Forms an array of tasks"""
    tasks = []
    for _ in range(total_req):
        tasks.append(asyncio.create_task(makepost_req(url, session)))
    return tasks


async def send_requests(url, total_req=1):
    """Keeps track of all requests"""
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(url, session, total_req)
        return await asyncio.gather(*tasks)


async def make_async_requests(url, total_req=1):
    """Makes sure that 'total_req' reuqests were successfull"""
    success, sended_req = 0, 0
    while success < total_req:
        remaining_requests = total_req - success
        responses = await send_requests(url, remaining_requests)
        for succs in responses:
            success += succs
        sended_req += remaining_requests
    
    print('Success rate: {}% ({}/{})'.format(success * 100/ sended_req, success, sended_req))


def start_requests(url, total_req=1):
    """Starts the requests sending process"""
    asyncio.run(make_async_requests(url, total_req))
