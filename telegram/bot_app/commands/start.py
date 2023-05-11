import os

from aiogram import types
from aiogram.dispatcher import FSMContext

from .. import messages
from ..app import dp, bot
from ..data_fetcher import Account
from ..keyboards import keyboard_from_list
from ..states import BaseStates, AccountStates


@dp.message_handler(commands='start', state='*')
async def start(message: types.Message, state: FSMContext):
    await BaseStates.start.set()

    account = Account(message.from_user)
    if await account.login():
        async with state.proxy() as data:
            data['token'] = account.token
        keyboard = await keyboard_from_list(['Income', 'Expense'])
        await message.answer(text=messages.WELCOME_MESSAGE, reply_markup=keyboard)
    else:
        keyboard = await keyboard_from_list(['USD', 'RUB', 'KZT'])
        await message.answer(text=messages.CURRENCY, reply_markup=keyboard)
        await AccountStates.create.set()
        async with state.proxy() as data:
            data['account'] = account


@dp.message_handler(commands='check', state='*')
async def check(message: types.Message, state: FSMContext):
    await BaseStates.start.set()
    async with state.proxy() as data:
        token = data.get('token')
        if not token:
            await message.answer(text=messages.ERROR)
            return
        account = Account(message.from_user, token=token)
        res = await account.get()
        if res is None:
            await message.answer(text=messages.ERROR)
            return
        amount = res.get('amount')
        await message.answer(text=f'Your amount of money is {amount}')


@dp.callback_query_handler(lambda c: c.data in ['USD', 'RUB', 'KZT'], state=AccountStates)
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
        keyboard = await keyboard_from_list(['Income', 'Expense'])
        await bot.send_message(chat_id=callback_query.from_user.id, text=messages.WELCOME_MESSAGE,
                               reply_markup=keyboard)
    else:
        await bot.send_message(chat_id=callback_query.from_user.id, text=messages.ERROR)
    await BaseStates.start.set()


@dp.callback_query_handler(state=AccountStates)
async def process_invalid_currency_selection(callback_query: types.CallbackQuery):
    message = f"Please select a valid currency"
    keyboard = await keyboard_from_list(['USD', 'RUB', 'KZT'])
    await bot.send_message(chat_id=callback_query.from_user.id, text=message, reply_markup=keyboard)
