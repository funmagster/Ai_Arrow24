import aiohttp
from config import url_backend


async def fetch_data(data, prefix):
    async with aiohttp.ClientSession() as session:
        async with session.post(url_backend + prefix, json=data) as response:
            response_data = await response.json()
            print(response_data)
            return response_data
