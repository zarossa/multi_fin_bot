from aiogram import types
from aiogram.dispatcher import FSMContext

from . import messages
from .app import dp, bot
from .data_fetcher import put_currency
from .keyboards import inline_kb
from .states import WorkStates


async def check_token(message: types.Message, data) -> bool:
    if data.get('token') is None:
        await message.answer('/start')
        return False
    return True


@dp.message_handler(commands='choose_currency', state='*')
async def choose_currency(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not await check_token(message, data):
            return
        await message.answer(f'Choose a currency', reply_markup=inline_kb)


@dp.callback_query_handler(lambda c: c.data in ['USD', 'RUB', 'KZT'], state=WorkStates.start)
async def button_click_call_back_currency(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    currency = callback_query.data
    async with state.proxy() as data:
        res = await put_currency(token=data.get('token'), currency=currency)
        if not res:
            await bot.send_message(callback_query.from_user.id, messages.ERROR)
            return
        await bot.send_message(callback_query.from_user.id, messages.SUCCESS)
