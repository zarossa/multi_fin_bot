from .commands import TgBot
from django.core.management.base import BaseCommand

import logging

logging.basicConfig(level=logging.INFO)


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
        TgBot()
