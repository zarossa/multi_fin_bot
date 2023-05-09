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


async def keyboard_from_dict(buttons: list, text_key: str = 'name', callback_key: str = 'pk') -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    [keyboard.add(InlineKeyboardButton(text=button.get(text_key),
                                       callback_data=button.get(callback_key))) for button in buttons]
    return keyboard
