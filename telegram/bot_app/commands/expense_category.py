from aiogram import types
from aiogram.dispatcher import FSMContext

from .. import messages
from ..app import dp, bot
from ..data_fetcher import ExpenseCategory
from ..keyboards import base_keyboard, keyboard_from_dict
from ..states import BaseStates, CategoryExpenseStates


@dp.message_handler(commands='category_expense', state=[BaseStates, CategoryExpenseStates])
async def start(message: types.Message, state: FSMContext):
    await BaseStates.start.set()
    async with state.proxy() as data:
        token = data.get('token')
        if not token:
            await message.answer(text=messages.ERROR)
            return
        await CategoryExpenseStates.base.set()
        expense_category = ExpenseCategory(token=token)
        expense_categories = await expense_category.get()
        data['data'] = expense_category

    if expense_categories is None:
        await message.answer(messages.ERROR)
        return
    if expense_categories:
        categories_list = '\n'.join([f'- {category.get("name")}' for category in expense_categories])
        keyboard = await base_keyboard()
        await message.answer(f'Your categories:\n{categories_list}', reply_markup=keyboard)
        return
    else:
        keyboard = await base_keyboard(is_blank=True)
        await message.answer(f'You don\'t have any category', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'Create new', state=CategoryExpenseStates.base)
async def create_category_expense(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        category = data.get('data')
        if not category.token:
            await bot.send_message(chat_id=callback_query.from_user.id, text=messages.ERROR)
            await BaseStates.start.set()
            return
        await bot.send_message(callback_query.from_user.id, "Please provide the name of a new expense category")
        await CategoryExpenseStates.create.set()
        data['data'] = category


@dp.message_handler(state=CategoryExpenseStates.create)
async def create_category_expense_process(message: types.Message, state: FSMContext):
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
        await CategoryExpenseStates.base.set()
        await start(message, state)


@dp.callback_query_handler(lambda c: c.data == 'Edit', state=CategoryExpenseStates.base)
async def edit_category_expense(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        category = data.get('data')
        if not category.token:
            await bot.send_message(chat_id=callback_query.from_user.id, text=messages.ERROR)
            await BaseStates.start.set()
            return
        await category.get()
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Please choose an expense category to edit",
                               reply_markup=await keyboard_from_dict(category.categories))
        await CategoryExpenseStates.edit.set()
        data['token'] = category.token


@dp.callback_query_handler(state=CategoryExpenseStates.edit)
async def edit_category_expense_process(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        category = data.get('data')
        if not category.token:
            await bot.send_message(chat_id=callback_query.from_user.id, text=messages.ERROR)
            await BaseStates.start.set()
            return

        await bot.send_message(callback_query.from_user.id, "Please provide the name of the expense category")
        await CategoryExpenseStates.edit_name.set()
        data['data'] = category
        data['category'] = callback_query.data


@dp.message_handler(state=CategoryExpenseStates.edit_name)
async def edit_category_expense_get_name(message: types.Message, state: FSMContext):
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
        await CategoryExpenseStates.base.set()
        await start(message, state)


@dp.callback_query_handler(lambda c: c.data == 'Delete', state=CategoryExpenseStates.base)
async def delete_category_expense(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        category = data.get('data')
        if not category.token:
            await bot.send_message(chat_id=callback_query.from_user.id, text=messages.ERROR)
            await BaseStates.start.set()
            return
        await category.get()
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Please choose an expense category to delete",
                               reply_markup=await keyboard_from_dict(category.categories))
        await CategoryExpenseStates.delete.set()
        data['data'] = category


@dp.callback_query_handler(state=CategoryExpenseStates.delete)
async def delete_category_expense_process(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        category = data.get('data')
        if not category.token:
            await bot.send_message(chat_id=callback_query.from_user.id, text=messages.ERROR)
            return

        category_id = callback_query.data
        success = await category.delete(category_id)
        if success:
            await bot.send_message(chat_id=callback_query.from_user.id, text=f'You delete the category')
        else:
            await bot.send_message(chat_id=callback_query.from_user.id, text='Error deleting category')
        await CategoryExpenseStates.base.set()
        await start(callback_query.message, state)
