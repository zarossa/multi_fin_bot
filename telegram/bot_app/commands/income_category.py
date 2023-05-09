from aiogram import types
from aiogram.dispatcher import FSMContext

from .. import messages
from ..app import dp, bot
from ..data_fetcher import IncomeCategory
from ..keyboards import category_keyboard, keyboard_from_list, keyboard_from_dict
from ..states import BaseStates, CategoryIncomeStates


@dp.message_handler(commands='category_income', state=[BaseStates, CategoryIncomeStates])
async def start(message: types.Message, state: FSMContext):
    await BaseStates.start.set()
    async with state.proxy() as data:
        token = data.get('token')
        if not token:
            await message.answer(text=messages.ERROR)
            return
        await CategoryIncomeStates.base.set()
        income_category = IncomeCategory(token=token)
        income_categories = await income_category.get()
        data['data'] = income_category

    if income_categories is None:
        await message.answer(messages.ERROR)
        return
    if income_categories:
        categories_list = '\n'.join([f'- {category.get("name")}' for category in income_categories])
        keyboard = await category_keyboard()
        await message.answer(f'Your categories:\n{categories_list}', reply_markup=keyboard)
        return
    else:
        keyboard = await category_keyboard(is_blank=True)
        await message.answer(f'You don\'t have any category', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'Create new', state=CategoryIncomeStates.base)
async def create_category_income(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        category = data.get('data')
        if not category.token:
            await bot.send_message(chat_id=callback_query.from_user.id, text=messages.ERROR)
            await BaseStates.start.set()
            return
        await bot.send_message(callback_query.from_user.id, "Please provide the name of a new income category")
        await CategoryIncomeStates.create.set()
        data['data'] = category


@dp.message_handler(state=CategoryIncomeStates.create)
async def create_category_income_process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        category = data.get('data')
        if not category.token:
            await message.answer(text=messages.ERROR)
            return

        category_name = message.text
        success = await category.create(category_name)
        if success:
            await message.answer(text=f'You create a new category "{category_name}"')
        else:
            await message.answer(text='Error creating category')
        await CategoryIncomeStates.base.set()
        await start(message, state)


@dp.callback_query_handler(lambda c: c.data == 'Edit', state=CategoryIncomeStates.base)
async def edit_category_income(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        category = data.get('data')
        if not category.token:
            await bot.send_message(chat_id=callback_query.from_user.id, text=messages.ERROR)
            await BaseStates.start.set()
            return
        await category.get()
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Please choose an income category to edit",
                               reply_markup=await keyboard_from_dict(category.categories))
        await CategoryIncomeStates.edit.set()
        data['token'] = category.token


@dp.callback_query_handler(state=CategoryIncomeStates.edit)
async def edit_category_income_process(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        category = data.get('data')
        if not category.token:
            await bot.send_message(chat_id=callback_query.from_user.id, text=messages.ERROR)
            await BaseStates.start.set()
            return

        await bot.send_message(callback_query.from_user.id, "Please provide the name of the income category")
        await CategoryIncomeStates.edit_name.set()
        data['data'] = category
        data['category'] = callback_query.data


@dp.message_handler(state=CategoryIncomeStates.edit_name)
async def edit_category_income_get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        category = data.get('data')
        category_id = data.get('category')
        if not category.token:
            await message.answer(text=messages.ERROR)
            return

        category_name = message.text
        success = await category.update(category_id, category_name)
        if success:
            await message.answer(text=f'The category has been successfully renamed to "{category_name}"')
        else:
            await message.answer(text='Error renaming category')
        await CategoryIncomeStates.base.set()
        await start(message, state)
