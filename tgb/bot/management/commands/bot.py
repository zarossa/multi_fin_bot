# from aiogram.utils import executor
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand

import os
from aiogram import Bot, Dispatcher, types, executor

from bot.models import User, Currency

# from bot.models import User

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


def log_error(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f'ERROR! {e}')
            raise
    return inner


class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        bot = Bot(token=TOKEN)
        dp = Dispatcher(bot)

        @log_error
        @dp.message_handler(commands=['start'])
        async def cmd_start(message: types.Message):
            preferred_currency = await sync_to_async(Currency.objects.get)(code="USD")

            user, created = await sync_to_async(User.objects.update_or_create)(
                telegram_id=message.from_user.id,
                defaults={
                    'name': message.from_user.first_name,
                    'preferred_currency': preferred_currency
                }
            )
            text = (
                f"Hi {user.name}!\n"
                "I'm the MultiFinBot, and I'm here to help you track your finances in multiple currencies.\n"
                "To get started, please type /help."
            )
            await message.reply(text)

        executor.start_polling(dp, skip_updates=True)
