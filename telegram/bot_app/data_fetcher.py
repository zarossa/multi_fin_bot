import aiohttp
import os

from aiogram.types import User

PASSWORD = os.getenv('PASSWORD')

HOST = os.getenv('HOST')
USER_API_REGISTER = f"{HOST}{os.getenv('USER_API_REGISTER')}"
USER_API_LOGIN = f"{HOST}{os.getenv('USER_API_LOGIN')}"
ACCOUNT_API = f"{HOST}{os.getenv('ACCOUNT_API')}"

CATEGORY_INCOME_API = f"{HOST}{os.getenv('CATEGORY_INCOME_API')}"
INCOME_API = f"{HOST}{os.getenv('INCOME_API')}"

CATEGORY_EXPENSE_API = f"{HOST}{os.getenv('CATEGORY_EXPENSE_API')}"
EXPENSE_API = f"{HOST}{os.getenv('EXPENSE_API')}"


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
                    return data
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


class Income:
    def __init__(self, token: str):
        self.token = token
        self.incomes = []

    async def get(self) -> list | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    INCOME_API,
                    headers={'Authorization': f'Token {self.token}'}) as response:
                if response.status == 200:
                    data = await response.json()
                    self.incomes = data
                    return data
                return None

    async def create(self, amount: float, currency: int, category: int) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    INCOME_API,
                    headers={'Authorization': f'Token {self.token}'},
                    json={'amount': float(amount), 'currency': currency, 'category': category}) as response:
                if response.status == 201:
                    return True
                return False

    async def delete(self, pk: int) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                    f'{INCOME_API}{pk}/',
                    headers={'Authorization': f'Token {self.token}'}) as response:
                if response.status == 204:
                    return True
                return False


class ExpenseCategory:
    def __init__(self, token: str):
        self.token = token
        self.categories = []

    async def get(self) -> list | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    CATEGORY_EXPENSE_API,
                    headers={'Authorization': f'Token {self.token}'}) as response:
                if response.status == 200:
                    data = await response.json()
                    self.categories = data
                    return data
                return None

    async def create(self, category_name: str) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    CATEGORY_EXPENSE_API,
                    headers={'Authorization': f'Token {self.token}'},
                    json={'name': category_name}) as response:
                if response.status == 201:
                    return True
                return False

    async def update(self, pk: int, name: str) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.put(
                    f'{CATEGORY_EXPENSE_API}{pk}/',
                    headers={'Authorization': f'Token {self.token}'},
                    json={'name': name}) as response:
                if response.status == 200:
                    return True
                return False

    async def delete(self, pk: int) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                    f'{CATEGORY_EXPENSE_API}{pk}/',
                    headers={'Authorization': f'Token {self.token}'}) as response:
                if response.status == 204:
                    return True
                return False


class Expense:
    def __init__(self, token: str):
        self.token = token
        self.incomes = []

    async def get(self) -> list | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    EXPENSE_API,
                    headers={'Authorization': f'Token {self.token}'}) as response:
                if response.status == 200:
                    data = await response.json()
                    self.incomes = data
                    return data
                return None

    async def create(self, amount: float, currency: int, category: int) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    EXPENSE_API,
                    headers={'Authorization': f'Token {self.token}'},
                    json={'amount': float(amount), 'currency': currency, 'category': category}) as response:
                if response.status == 201:
                    return True
                return False

    async def delete(self, pk: int) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                    f'{EXPENSE_API}{pk}/',
                    headers={'Authorization': f'Token {self.token}'}) as response:
                if response.status == 204:
                    return True
                return False
