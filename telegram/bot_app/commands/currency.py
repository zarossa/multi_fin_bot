from aiogram import types
from aiogram.dispatcher import FSMContext

from .. import messages
from ..app import dp, bot
from ..data_fetcher import Currency, AccountCurrency
from ..keyboards import base_keyboard, keyboard_from_dict
from ..states import StartStates, CurrencyStates


@dp.message_handler(commands='currency', state='*')
async def start(message: types.Message, state: FSMContext):
    await StartStates.start.set()
    async with state.proxy() as data:
        token = data.get('token')
        if not token:
            await message.answer(text=messages.ERROR)
            return
        await CurrencyStates.base.set()
        currency = AccountCurrency(token=token)
        currencies = await currency.get()
        data['data'] = currency

    if currencies is None:
        await message.answer(messages.ERROR)
        return
    if currencies:
        currencies_list = '\n'.join([f'- {cur.get("name")}' for cur in currencies])
        keyboard = await base_keyboard(is_adding=True)
        await message.answer(f'Your currencies:\n{currencies_list}', reply_markup=keyboard)
        return
    else:
        keyboard = await base_keyboard(is_blank=True, is_adding=True)
        await message.answer(f'You don\'t have any currency', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'Add', state=CurrencyStates.base)
async def add_currency(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        currency = data.get('data')
        if not currency.token:
            await bot.send_message(chat_id=callback_query.from_user.id, text=messages.ERROR)
            await StartStates.start.set()
            return
        all_currency = Currency()
        all_currency = await all_currency.get()
        await bot.send_message(callback_query.from_user.id, "Please choose a currency to add",
                               reply_markup=await keyboard_from_dict(all_currency))
        await CurrencyStates.add.set()
        data['data'] = currency


@dp.callback_query_handler(state=CurrencyStates.add)
async def add_currency_process(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        currency = data.get('data')
        if not currency.token:
            await bot.send_message(chat_id=callback_query.from_user.id, text=messages.ERROR)
            return

        new_currency = callback_query.data
        success = await currency.create(new_currency)
        if success:
            await bot.send_message(chat_id=callback_query.from_user.id, text=f'You add a new currency')
        else:
            await bot.send_message(chat_id=callback_query.from_user.id, text='Error adding currency')
        await CurrencyStates.base.set()
        await start(callback_query.message, state)


@dp.callback_query_handler(lambda c: c.data == 'Delete', state=CurrencyStates.base)
async def delete_currency(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        currency = data.get('data')
        if not currency.token:
            await bot.send_message(chat_id=callback_query.from_user.id, text=messages.ERROR)
            await StartStates.start.set()
            return
        currencies = await currency.get()
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Please choose a currency to delete",
                               reply_markup=await keyboard_from_dict(currencies))
        await CurrencyStates.delete.set()
        data['data'] = currency


@dp.callback_query_handler(state=CurrencyStates.delete)
async def delete_currency_process(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        currency = data.get('data')
        if not currency.token:
            await bot.send_message(chat_id=callback_query.from_user.id, text=messages.ERROR)
            return

        currency_id = callback_query.data
        success = await currency.delete(currency_id)
        if success:
            await bot.send_message(chat_id=callback_query.from_user.id, text=f'You delete the currency')
        else:
            await bot.send_message(chat_id=callback_query.from_user.id, text='Error deleting currency')
        await CurrencyStates.base.set()
        await start(callback_query.message, state)
