import os

import aiohttp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import User

from . import messages

from .app import dp
from .states import WorkStates

USER_API_REGISTER = os.getenv('USER_API_REGISTER')
USER_API_LOGIN = os.getenv('USER_API_LOGIN')
PASSWORD = os.getenv('PASSWORD')


async def login_user(username: int, password: str = PASSWORD):
    async with aiohttp.ClientSession() as session:
        async with session.post(USER_API_LOGIN, json={
            'username': username,
            'password': password
        }) as response:
            data = await response.json()
            return data.get('auth_token')


async def register_user(telegram_user: User, password: str = PASSWORD):
    async with aiohttp.ClientSession() as session:
        async with session.post(USER_API_REGISTER, json={
            'username': telegram_user.id,
            'first_name': telegram_user.first_name,
            'password': password
        }) as response:
            if response.status == 201:
                data = await response.json()
                # Process the response data if needed
                return messages.REGISTER
            else:
                # Handle the error case
                return 'Error creating user'


@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    await WorkStates.start.set()

    token = await login_user(username=message.from_user.id)

    if not token:
        answer = await register_user(message.from_user)
        await message.reply(answer)
        token = await login_user(username=message.from_user.id)
    await message.reply(f'{messages.WELCOME_MESSAGE}\nYour token is:\n{token}')
