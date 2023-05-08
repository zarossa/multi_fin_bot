from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

currencies = ['USD', 'RUB', 'KZT']
currency_kb = InlineKeyboardMarkup()

[currency_kb.add(InlineKeyboardButton(currency, callback_data=currency)) for currency in currencies]


async def category_keyboard(is_blank: bool = False):
    buttons = ['Create new']
    if not is_blank:
        buttons.extend(['Delete', 'Edit'])
    keyboard = InlineKeyboardMarkup()
    [keyboard.add(InlineKeyboardButton(button, callback_data=button)) for button in buttons]
    return keyboard
