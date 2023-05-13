import aiohttp
import os

from aiogram.types import User

PASSWORD = os.getenv('PASSWORD')

HOST = os.getenv('HOST')
USER_API_REGISTER = f"{HOST}{os.getenv('USER_API_REGISTER')}"
USER_API_LOGIN = f"{HOST}{os.getenv('USER_API_LOGIN')}"
ACCOUNT_API = f"{HOST}{os.getenv('ACCOUNT_API')}"

INCOME_API = f"{HOST}{os.getenv('INCOME_API')}"
CATEGORY_INCOME_API = f"{INCOME_API}{os.getenv('CATEGORY')}"

EXPENSE_API = f"{HOST}{os.getenv('EXPENSE_API')}"
CATEGORY_EXPENSE_API = f"{EXPENSE_API}{os.getenv('CATEGORY')}"


class Account:
    def __init__(self, telegram_user: User, password: str = PASSWORD, token: str = None):
        self.telegram_user = telegram_user
        self.password = password
        self.token = token
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

    async def get(self) -> dict | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    ACCOUNT_API,
                    headers={'Authorization': f'Token {self.token}'}) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                return None

    async def _delete_user(self) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                    ACCOUNT_API,
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
                    ACCOUNT_API,
                    headers={'Authorization': f'Token {self.token}'},
                    json={'currency_code': currency}) as response:
                if response.status == 201:
                    self.currency = currency
                    return True
                return False


class APIClient:
    BASE_URL = ''
    HEADERS = {}

    def __init__(self, token: str):
        self.token = token
        self.items = []

    async def get(self) -> list | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'{self.BASE_URL}',
                    headers={'Authorization': f'Token {self.token}', **self.HEADERS}) as response:
                if response.status == 200:
                    data = await response.json()
                    self.items = data
                    return data
                return None

    async def create(self, **kwargs) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    f'{self.BASE_URL}',
                    headers={'Authorization': f'Token {self.token}', **self.HEADERS},
                    json=kwargs) as response:
                if response.status == 201:
                    return True
                return False

    async def update(self, pk: int, name: str) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.put(
                    f'{self.BASE_URL}{pk}/',
                    headers={'Authorization': f'Token {self.token}', **self.HEADERS},
                    json={'name': name}) as response:
                if response.status == 200:
                    return True
                return False

    async def delete(self, pk: int) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                    f'{self.BASE_URL}{pk}/',
                    headers={'Authorization': f'Token {self.token}', **self.HEADERS}) as response:
                if response.status == 204:
                    return True
                return False


class BaseCategory(APIClient):
    async def create(self, category_name: str) -> bool:
        return await super().create(name=category_name)


class BaseTransaction(APIClient):
    async def create(self, amount: float, currency: int, category: int) -> bool:
        return await super().create(amount=float(amount), currency=currency, category=category)


class IncomeCategory(BaseCategory):
    BASE_URL = CATEGORY_INCOME_API


class Income(BaseTransaction):
    BASE_URL = INCOME_API


class ExpenseCategory(BaseCategory):
    BASE_URL = CATEGORY_EXPENSE_API


class Expense(BaseTransaction):
    BASE_URL = EXPENSE_API
