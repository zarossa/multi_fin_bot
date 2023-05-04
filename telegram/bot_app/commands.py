import os

import aiohttp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import User

from . import messages

from .app import dp
from .states import WorkStates

USER_API_URL = os.getenv('USER_API_URL')
USER_API_REGISTER = os.getenv('USER_API_REGISTER')

PASSWORD = os.getenv('PASSWORD')


async def get_user(telegram_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{USER_API_URL}{str(telegram_id)}/') as response:
            status = response.status
            if status == 200:
                return await response.json()
            return None


async def create_user(telegram_user: User):
    async with aiohttp.ClientSession() as session:
        async with session.post(USER_API_REGISTER, json={
            'username': telegram_user.id,
            'first_name': telegram_user.first_name,
            'password': PASSWORD
        }) as response:
            print(response, response.status)
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

    user = await get_user(message.from_user.id)
    if not user:
        answer = await create_user(message.from_user)
        await message.reply(answer)
        return
    async with state.proxy() as data:
        print(data)
        # user, created = await sync_to_async(TelegramUser.objects.get_or_create)(
        #     telegram_id=message.from_user.id,
        #     defaults={
        #         'name': message.from_user.first_name,
        #         'preferred_currency': preferred_currency
        #     }
        # )
        await message.reply(messages.WELCOME_MESSAGE)
