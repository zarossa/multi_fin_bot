import aiohttp
import os

WORDS_API_URL_RANDOM = os.getenv('WORDS_API_URL_RANDOM')


async def get_random():
    async with aiohttp.ClientSession() as session:
        async with session.get(WORDS_API_URL_RANDOM) as responce:
            return await responce.json()
