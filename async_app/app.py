import asyncio

import aiohttp
from aiohttp import web
import uvloop


async def hello(request):
    name = request.match_info.get('name', 'you')
    text = f'Hi {name}!'
    return web.Response(text=text)


async def get_page_text(session, address):
    async with session.get(address) as response:
        return await response.text()


async def download(request):
    loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession(loop=loop) as session:
        addresses_str = request.match_info.get('addresses', '')
        addresses = [f'https://{address}' for address in addresses_str.split(',')]

        futures = [get_page_text(session, address) for address in addresses]
        results = await asyncio.gather(*futures)
    to_return = '\n'.join([result[:100] for result in results])
    return web.Response(text=to_return)


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

application = web.Application()
application.router.add_get('/', hello)
application.router.add_get('/{name}', hello)
application.router.add_get('/download/{addresses}', download)

web.run_app(application)