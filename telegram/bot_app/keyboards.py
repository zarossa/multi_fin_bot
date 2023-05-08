from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

inline_button_USD = InlineKeyboardButton('USD', callback_data='USD')
inline_button_RUB = InlineKeyboardButton('RUB', callback_data='RUB')
inline_button_KZT = InlineKeyboardButton('KZT', callback_data='KZT')
currency_kb = InlineKeyboardMarkup()

currency_kb.add(inline_button_USD)
currency_kb.add(inline_button_RUB)
currency_kb.add(inline_button_KZT)
