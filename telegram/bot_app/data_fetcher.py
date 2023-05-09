import aiohttp
import os

from aiogram.types import User

PASSWORD = os.getenv('PASSWORD')

USER_API_REGISTER = os.getenv('USER_API_REGISTER')
USER_API_LOGIN = os.getenv('USER_API_LOGIN')
USER_API_DELETE = os.getenv('USER_API_DELETE')
ACCOUNT_API_CREATE = os.getenv('ACCOUNT_API_CREATE')

CATEGORY_INCOME_API = os.getenv('CATEGORY_INCOME_API')


class Account:
    def __init__(self, telegram_user: User, password: str = PASSWORD):
        self.telegram_user = telegram_user
        self.password = password
        self.token = None
        self.currency = None

    async def login(self) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.post(USER_API_LOGIN, json={
                'username': self.telegram_user.id,
                'password': self.password
            }) as response:
                if response.status == 200:
                    json = await response.json()
                    self.token = json.get('auth_token')
                    return True
                return False

    async def register(self, currency: str) -> bool:
        is_created = await self._create_user()
        if is_created:
            is_logged_in = await self.login()
            if is_logged_in:
                is_registered = await self._create_account(currency)
                if is_registered:
                    return True
                await self._delete_user()
        return False

    async def _delete_user(self) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                    USER_API_DELETE,
                    headers={'Authorization': f'Token {self.token}'}) as response:
                if response.status == 204:
                    return True
                return False

    async def _create_user(self) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.post(USER_API_REGISTER, json={
                'username': self.telegram_user.id,
                'first_name': self.telegram_user.first_name,
                'password': self.password
            }) as response:
                if response.status == 201:
                    return True
                return False

    async def _create_account(self, currency: str) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    ACCOUNT_API_CREATE,
                    headers={'Authorization': f'Token {self.token}'},
                    json={'currency_code': currency}) as response:
                if response.status == 201:
                    self.currency = currency
                    return True
                return False


class IncomeCategory:
    def __init__(self, token: str):
        self.token = token
        self.categories = []

    async def get(self) -> list | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    CATEGORY_INCOME_API,
                    headers={'Authorization': f'Token {self.token}'}) as response:
                if response.status == 200:
                    data = await response.json()
                    self.categories = data
                    return data  # [cls(category.get('name')) for category in data]
                return None

    async def create(self, category_name: str) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    CATEGORY_INCOME_API,
                    headers={'Authorization': f'Token {self.token}'},
                    json={'name': category_name}) as response:
                if response.status == 201:
                    return True
                return False

    async def update(self, pk: int, name: str) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.put(
                    f'{CATEGORY_INCOME_API}{pk}/',
                    headers={'Authorization': f'Token {self.token}'},
                    json={'name': name}) as response:
                if response.status == 200:
                    return True
                return False

    async def delete(self, pk: int) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                    f'{CATEGORY_INCOME_API}{pk}/',
                    headers={'Authorization': f'Token {self.token}'}) as response:
                if response.status == 204:
                    return True
                return False

