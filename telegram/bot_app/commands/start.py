import os

from aiogram import types
from aiogram.dispatcher import FSMContext

from .. import messages
from ..app import dp, bot
from ..data_fetcher import login_user, register_user
from ..keyboards import currency_kb
from ..states import WorkStates

USER_API_REGISTER = os.getenv('USER_API_REGISTER')
USER_API_LOGIN = os.getenv('USER_API_LOGIN')
PASSWORD = os.getenv('PASSWORD')


@dp.message_handler(commands='start', state='*')
async def start(message: types.Message, state: FSMContext):
    await WorkStates.start.set()
    token = await login_user(message.from_user)

    if not token:
        await message.answer(text=messages.CURRENCY, reply_markup=currency_kb)
        await WorkStates.create_user.set()
        return

    async with state.proxy() as data:
        data['token'] = token
    await message.answer(messages.WELCOME_MESSAGE)


@dp.callback_query_handler(lambda c: c.data in ['USD', 'RUB', 'KZT'], state=WorkStates.create_user)
async def account_creating(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    currency = callback_query.data
    await WorkStates.start.set()
    token = await register_user(callback_query.from_user, currency)
    if not token:
        await bot.send_message(chat_id=callback_query.from_user.id, text=messages.ERROR)
        return
    async with state.proxy() as data:
        data['token'] = token
    await bot.send_message(chat_id=callback_query.from_user.id, text=messages.WELCOME_MESSAGE)


@dp.callback_query_handler(state=WorkStates.create_user)
async def process_invalid_currency_selection(callback_query: types.CallbackQuery):
    message = f"Please select a valid currency"
    await bot.send_message(chat_id=callback_query.from_user.id, text=message, reply_markup=currency_kb)
