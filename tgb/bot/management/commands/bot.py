from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand

import os
import logging
from aiogram import Bot, Dispatcher, types, executor

from bot.models import User, Currency

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
logging.basicConfig(level=logging.INFO)


def log_error(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f'ERROR! {e}')
            raise
    return inner


class TgBot:
    def __init__(self):
        self.bot = Bot(token=TOKEN)
        self.dp = Dispatcher(self.bot)
        self.dp.register_message_handler(self.cmd_start, commands=["start"])
        self.dp.register_message_handler(self.cmd_help, commands=["help"])
        executor.start_polling(self.dp)  #, on_shutdown=self.stop)

    async def cmd_start(self, message: types.Message):
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
        await message.answer(text)
        # await message.reply(text)

    async def cmd_help(self, message: types.Message):
        help_message = (
            "This is a demo bot. Here are the available commands:\n"
            "/start - start the bot\n"
            "/help - display this help message"
        )
        await message.answer(help_message)

    async def stop(self):
        await self.bot.close()


class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        TgBot()
