from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


async def category_keyboard(is_blank: bool = False) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    buttons = ['Create new']
    if not is_blank:
        buttons.extend(['Delete', 'Edit'])
    [keyboard.add(InlineKeyboardButton(button, callback_data=button)) for button in buttons]
    return keyboard


async def keyboard_from_list(buttons: list) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    [keyboard.add(InlineKeyboardButton(button, callback_data=button)) for button in buttons]
    return keyboard
