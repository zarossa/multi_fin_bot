from aiogram import types
from aiogram.dispatcher import FSMContext

from .. import messages
from ..app import dp, bot
from ..data_fetcher import IncomeCategory
from ..keyboards import category_keyboard
from ..states import WorkStates


@dp.message_handler(commands='category_income', state=[WorkStates.start, WorkStates.category_income])
async def start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        token = data.get('token')
        if not token:
            await message.answer(text=messages.ERROR)
            await WorkStates.start.set()
            return
        await WorkStates.category_income.set()
        data['token'] = token

    income_categories = await IncomeCategory.get(token)
    if income_categories is None:
        await message.answer(messages.ERROR)
        return
    if income_categories:
        categories_list = '\n'.join([f'- {category.name}' for category in income_categories])
        keyboard = await category_keyboard()
        await message.answer(f'Your categories:\n{categories_list}', reply_markup=keyboard)
        return
    else:
        keyboard = await category_keyboard(is_blank=True)
        await message.answer(f'You don\'t have any category', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'Create new', state=WorkStates.category_income)
async def create_category_income(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Please provide the name of a new income category")
    async with state.proxy() as data:
        token = data.get('token')
    await WorkStates.category_income_create.set()
    async with state.proxy() as data:
        data['token'] = token


@dp.message_handler(state=WorkStates.category_income_create)
async def create_category_income_process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        token = data.get('token')
        if not token:
            await message.answer(text=messages.ERROR)
            return

        category_name = message.text
        success = await IncomeCategory.create(token, category_name)
        if success:
            await message.answer(text=f'You create a new category "{category_name}"')
        else:
            await message.answer(text='Error creating category')
        await WorkStates.category_income.set()
        await start(message, state)
