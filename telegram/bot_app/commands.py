import os

from aiogram import types
from aiogram.dispatcher import FSMContext

from . import messages

from .app import dp
from .data_fetcher import login_user, register_user
from .states import WorkStates

USER_API_REGISTER = os.getenv('USER_API_REGISTER')
USER_API_LOGIN = os.getenv('USER_API_LOGIN')
PASSWORD = os.getenv('PASSWORD')


@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    await WorkStates.start.set()

    token = await login_user(message.from_user)

    if not token.get('auth_token'):
        is_registered = await register_user(message.from_user)
        if not is_registered:
            await message.reply(messages.ERROR)
            return
        await message.reply(messages.REGISTER)
        token = await login_user(message.from_user)
    async with state.proxy() as data:
        data['token'] = token.get('auth_token')
    await message.reply(messages.WELCOME_MESSAGE)
