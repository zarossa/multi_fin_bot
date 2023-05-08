import aiohttp
import os

from aiogram.types import User

USER_API_REGISTER = os.getenv('USER_API_REGISTER')
USER_API_LOGIN = os.getenv('USER_API_LOGIN')
USER_API_DELETE = os.getenv('USER_API_DELETE')
ACCOUNT_API_CREATE = os.getenv('ACCOUNT_API_CREATE')

CATEGORY_INCOME_API = os.getenv('CATEGORY_INCOME_API')


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


class IncomeCategory:
    def __init__(self, name: str):
        self.name = name

    @classmethod
    async def get(cls, token: str) -> list | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(CATEGORY_INCOME_API, headers={'Authorization': f'Token {token}'}) as response:
                if response.status == 200:
                    data = await response.json()
                    return [cls(category.get('name')) for category in data]
                return None

    @classmethod
    async def create(cls, token: str, category_name: str) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    CATEGORY_INCOME_API,
                    headers={'Authorization': f'Token {token}'},
                    json={'name': category_name}) as response:
                if response.status == 201:
                    return True
                return False
