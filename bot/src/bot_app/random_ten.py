from aiogram import types
from aiogram.dispatcher import FSMContext

from .app import dp
from .data_fetcher import get_random
from .keyboards import inline_kb
from .states import GameStates


@dp.message_handler(commands='train_ten', state='*')
async def train_ten(message: types.Message, state: FSMContext):
    await GameStates.random_ten.set()
    res = await get_random()
    async with state.proxy() as data:
        data['step'] = 1
        data['answer'] = res.get('gender')
        data['word'] = res.get('word')
        await message.reply(f'{data["step"]} of 10. Word is { data["word"] }', reply_markup=inline_kb)
