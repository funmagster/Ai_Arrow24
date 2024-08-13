import aiohttp
import asyncio


async def fetch_data(data):
    async with aiohttp.ClientSession() as session:
        await asyncio.sleep(100000)
        return {1: 1, 2: 2}
        # async with session.get(f'https://example.com/api/generate_game/?q={data}') as response:
        #     data = await response.json()
        #     return data
