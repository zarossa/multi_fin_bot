import aiohttp
import os

from aiogram.types import User

USER_API_REGISTER = os.getenv('USER_API_REGISTER')
USER_API_LOGIN = os.getenv('USER_API_LOGIN')
CURRENCY_API_URL = os.getenv('CURRENCY_API_URL')
PASSWORD = os.getenv('PASSWORD')


async def register_user(telegram_user: User) -> dict | None:
    async with aiohttp.ClientSession() as session:
        async with session.post(USER_API_REGISTER, json={
            'username': telegram_user.id,
            'first_name': telegram_user.first_name,
            'password': PASSWORD
        }) as response:
            status = response.status
            if status == 201:
                return await response.json()
            return None


async def login_user(telegram_user: User) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(USER_API_LOGIN, json={
            'username': telegram_user.id,
            'password': PASSWORD
        }) as response:
            return await response.json()


async def put_currency(token: str, currency: str):
    async with aiohttp.ClientSession() as session:
        async with session.put(
                CURRENCY_API_URL,
                headers={'Authorization': f'Token {token}'},
                json={'currency_code': currency}) as response:
            status = response.status
            if status == 200:
                return await response.json()
            return None
