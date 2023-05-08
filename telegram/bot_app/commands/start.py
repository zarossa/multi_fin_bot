import os

from aiogram import types
from aiogram.dispatcher import FSMContext

from .. import messages
from ..app import dp, bot
from ..data_fetcher import Account
from ..keyboards import currency_kb
from ..states import WorkStates


@dp.message_handler(commands='start', state='*')
async def start(message: types.Message, state: FSMContext):
    await WorkStates.start.set()

    account = Account(message.from_user)
    if await account.login():
        async with state.proxy() as data:
            data['token'] = account.token
        await message.answer(messages.WELCOME_MESSAGE)
    else:
        await message.answer(text=messages.CURRENCY, reply_markup=currency_kb)
        await WorkStates.create_user.set()
        async with state.proxy() as data:
            data['account'] = account


@dp.callback_query_handler(lambda c: c.data in ['USD', 'RUB', 'KZT'], state=WorkStates.create_user)
async def account_creating(callback_query: types.CallbackQuery, state: FSMContext):
    currency = callback_query.data
    async with state.proxy() as data:
        account = data.get('account')

    if not account:
        await bot.send_message(chat_id=callback_query.from_user.id, text=messages.ERROR)
        return
    if await account.register(currency):
        async with state.proxy() as data:
            data['token'] = account.token
        await bot.send_message(chat_id=callback_query.from_user.id, text=messages.WELCOME_MESSAGE)
    else:
        await bot.send_message(chat_id=callback_query.from_user.id, text=messages.ERROR)
    await WorkStates.start.set()


@dp.callback_query_handler(state=WorkStates.create_user)
async def process_invalid_currency_selection(callback_query: types.CallbackQuery):
    message = f"Please select a valid currency"
    await bot.send_message(chat_id=callback_query.from_user.id, text=message, reply_markup=currency_kb)
