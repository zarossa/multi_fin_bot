from aiogram import types
from aiogram.dispatcher import FSMContext

from .. import messages
from ..app import dp, bot
from ..data_fetcher import Expense, ExpenseCategory, AccountCurrency
from ..keyboards import keyboard_from_dict
from ..states import StartStates, ExpenseStates


@dp.callback_query_handler(lambda c: c.data == 'Expense', state=[StartStates, ExpenseStates])
async def start(callback_query: types.CallbackQuery, state: FSMContext):
    await StartStates.start.set()
    async with state.proxy() as data:
        token = data.get('token')
        if not token:
            await bot.send_message(chat_id=callback_query.from_user.id, text=messages.ERROR)
            return
        await ExpenseStates.base.set()
        expense = Expense(token=token)
        expense_categories = await ExpenseCategory(token=token).get()

        expense_list = await expense.get()
        data['data'] = expense_list

    if expense_categories is None:
        await bot.send_message(chat_id=callback_query.from_user.id, text=messages.ERROR)
        return
    if expense_categories:
        await ExpenseStates.create.set()
        async with state.proxy() as data:
            data['expense'] = expense
            data['token'] = token
        keyboard = await keyboard_from_dict(expense_categories, text_key='name', callback_key='pk')
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f'Choose a category:', reply_markup=keyboard)
    else:
        await StartStates.start.set()
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f'You don\'t have any expense category\nCreate new one here: /category_expense')


@dp.callback_query_handler(state=ExpenseStates.create)
async def create_expense(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = callback_query.data
        token = data.get('token')
        await ExpenseStates.create_currency.set()

        currency = AccountCurrency(token=token)
        currencies = await currency.get()
        if currencies:
            keyboard = await keyboard_from_dict([cur.get('currency') for cur in currencies])
            await bot.send_message(callback_query.from_user.id, "Choose amount currency:", reply_markup=keyboard)
        else:
            await StartStates.start.set()
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=f'You don\'t have any currency\nAdd new one here: /currency')


@dp.callback_query_handler(state=ExpenseStates.create_currency)
async def create_expense_currency(callback_query: types.CallbackQuery, state: FSMContext):
    await ExpenseStates.create.set()
    async with state.proxy() as data:
        data['currency'] = callback_query.data
        await bot.send_message(callback_query.from_user.id, "Please enter the amount of expense:")


@dp.message_handler(state=ExpenseStates.create)
async def create_expense_process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        expense = data.get('expense')
        category = data.get('category')
        currency = data.get('currency')

        amount = message.text
        success = await expense.create(amount=amount, currency=currency, category=category)
        if success:
            await message.answer(text=f'You create a new expense')
        else:
            await message.answer(text='Error creating expense')
        await ExpenseStates.base.set()
        callback_query = types.CallbackQuery()
        callback_query.from_user = message.from_user
        await start(callback_query=callback_query, state=state)
