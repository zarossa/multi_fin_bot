import aiohttp
import os

from aiogram.types import User

USER_API_REGISTER = os.getenv('USER_API_REGISTER')
USER_API_LOGIN = os.getenv('USER_API_LOGIN')
USER_API_DELETE = os.getenv('USER_API_DELETE')
ACCOUNT_API_CREATE = os.getenv('ACCOUNT_API_CREATE')
PASSWORD = os.getenv('PASSWORD')


async def login_user(telegram_user: User) -> str | None:
    async with aiohttp.ClientSession() as session:
        async with session.post(USER_API_LOGIN, json={
            'username': telegram_user.id,
            'password': PASSWORD
        }) as response:
            json = await response.json()
            return json.get('auth_token')


async def delete_user(token: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.delete(
                USER_API_DELETE,
                headers={'Authorization': f'Token {token}'}) as response:
            if response.status == 204:
                return True
            return False


async def create_user(telegram_user: User) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post(USER_API_REGISTER, json={
            'username': telegram_user.id,
            'first_name': telegram_user.first_name,
            'password': PASSWORD
        }) as response:
            if response.status == 201:
                return True
            return False


async def create_account(token: str, currency: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post(
                ACCOUNT_API_CREATE,
                headers={'Authorization': f'Token {token}'},
                json={'currency_code': currency}) as response:
            if response.status == 201:
                return True
            return False


async def register_user(telegram_user: User, currency: str) -> str | bool:
    is_created = await create_user(telegram_user)
    if is_created:
        token = await login_user(telegram_user)
        if not token:
            return False

        is_registered = await create_account(token, currency)
        if is_registered:
            return token
        await delete_user(token)
        return False
