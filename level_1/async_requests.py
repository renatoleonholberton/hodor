import asyncio
import aiohttp
from bs4 import BeautifulSoup, dammit


async def get_payload(res):
    """Generates the payload needed to be send"""
    soup = BeautifulSoup(await res.text(), 'html.parser')
    form = soup.form
    key_input = form.find('input', {'name': 'key'})

    return {
        'id': '2829',
        'holdthedoor': 'Submit',
        'key': key_input['value']
    }


async def make_request(url):
    """Mnages to make the requests needed to make a vote"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            payload = await get_payload(res)

        print(payload)
        async with session.post(url, data=payload) as res:
            print(await res.text())
            if len(await res.text()) > 100:
                print('Success!!!')
                return 1
            print('Fail!!!')
            return 0


async def get_tasks(url, total_req=1):
    """Creates an array of tasks"""
    tasks = []
    for _ in range(total_req):
            tasks.append(
                asyncio.create_task(make_request(url))
            )
    return tasks


async def send_requests(url, total_req=1):
    """Keeps track of each request"""
    tasks = await get_tasks(url, total_req)

    return await asyncio.gather(*tasks)


async def make_async_requests(url, total_req=1):
    """Makes sure that 'total_req' reuqests were successfull"""
    success, sended_req = 0, 0
    while success < total_req:
        remaining_req = total_req - success
        responses = await send_requests(url, remaining_req)
        for succs in responses:
            success += succs
        sended_req += remaining_req

    print('Success rate: {}% ({}/{})'.format(success * 100/ sended_req, success, sended_req))
    

def start_requests(url, total_req=1):
    """Starts the requests sending process"""
    asyncio.run(make_async_requests(url, total_req))


## 4: ???