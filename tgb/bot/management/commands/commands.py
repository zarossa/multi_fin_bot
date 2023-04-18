from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async

import os
from aiogram import Bot, Dispatcher, types, executor

from bot.models import User, Currency, CategoryIncome

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


class TgBot:
    def __init__(self):
        self.bot = Bot(token=TOKEN)
        self.dp = Dispatcher(self.bot)
        self.dp.register_message_handler(self.cmd_start, commands=["start"])
        self.dp.register_message_handler(self.cmd_help, commands=["help"])
        self.dp.register_callback_query_handler(self.new_category_callback, text="new_category")
        executor.start_polling(self.dp)  # , on_shutdown=self.stop)

    @staticmethod
    async def cmd_start(message: types.Message):
        preferred_currency = await sync_to_async(Currency.objects.get)(code="USD")

        user, created = await sync_to_async(User.objects.get_or_create)(
            telegram_id=message.from_user.id,
            defaults={
                'name': message.from_user.first_name,
                'preferred_currency': preferred_currency
            }
        )
        text = (
            f"Hi, {user.name}!\n"
            "I'm the MultiFinBot, and I'm here to help you track your finances in multiple currencies.\n"
            "To get started, please type /help."
        )
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text="New category", callback_data="new_category"))
        await message.answer(text, reply_markup=keyboard)

    @staticmethod
    async def cmd_help(message: types.Message):
        help_message = (
            "This is a demo bot. Here are the available commands:\n"
            "/start - start the bot\n"
            "/help - display this help message"
        )
        await message.answer(help_message)

    async def new_category_callback(self, query: types.CallbackQuery):
        user_id = query.from_user.id
        user = await sync_to_async(User.objects.get)(telegram_id=user_id)

        category_income = await sync_to_async(CategoryIncome.objects.create)(user=user, name='New category')

        text = f"Category {category_income.name} with ID {category_income.id} created successfully!"
        await self.bot.send_message(chat_id=user_id, text=text)

    async def stop(self):
        await self.bot.close()
