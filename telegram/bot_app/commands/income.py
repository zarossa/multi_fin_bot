from aiogram import types
from aiogram.dispatcher import FSMContext

from .. import messages
from ..app import dp, bot
from ..data_fetcher import Income, IncomeCategory, AccountCurrency
from ..keyboards import keyboard_from_dict
from ..states import StartStates, IncomeStates


@dp.callback_query_handler(lambda c: c.data == 'Income', state=[StartStates, IncomeStates])
async def start(callback_query: types.CallbackQuery, state: FSMContext):
    await StartStates.start.set()
    async with state.proxy() as data:
        token = data.get('token')
        if not token:
            await bot.send_message(chat_id=callback_query.from_user.id, text=messages.ERROR)
            return
        await IncomeStates.base.set()
        income = Income(token=token)
        income_categories = await IncomeCategory(token=token).get()

        income_list = await income.get()
        data['data'] = income_list

    if income_categories is None:
        await bot.send_message(chat_id=callback_query.from_user.id, text=messages.ERROR)
        return
    if income_categories:
        await IncomeStates.create.set()
        async with state.proxy() as data:
            data['income'] = income
            data['token'] = token
        keyboard = await keyboard_from_dict(income_categories, text_key='name', callback_key='pk')
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f'Choose a category:', reply_markup=keyboard)
    else:
        await StartStates.start.set()
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f'You don\'t have any income category\nCreate new one here: /category_income')


@dp.callback_query_handler(state=IncomeStates.create)
async def create_income(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = callback_query.data
        token = data.get('token')
        await IncomeStates.create_currency.set()

        currency = AccountCurrency(token=token)
        currencies = await currency.get()
        if currencies:
            keyboard = await keyboard_from_dict(currencies, callback_key='currency_pk')
            await bot.send_message(callback_query.from_user.id, "Choose amount currency:", reply_markup=keyboard)
        else:
            await StartStates.start.set()
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=f'You don\'t have any currency\nAdd new one here: /currency')


@dp.callback_query_handler(state=IncomeStates.create_currency)
async def create_income_currency(callback_query: types.CallbackQuery, state: FSMContext):
    await IncomeStates.create.set()
    async with state.proxy() as data:
        data['currency'] = callback_query.data
        await bot.send_message(callback_query.from_user.id, "Please enter the amount of income:")


@dp.message_handler(state=IncomeStates.create)
async def create_income_process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        income = data.get('income')
        category = data.get('category')
        currency = data.get('currency')

        amount = message.text
        success = await income.create(amount=amount, currency=currency, category=category)
        if success:
            await message.answer(text=f'You create a new income')
        else:
            await message.answer(text='Error creating income')
        await IncomeStates.base.set()
        callback_query = types.CallbackQuery()
        callback_query.from_user = message.from_user
        await start(callback_query=callback_query, state=state)
