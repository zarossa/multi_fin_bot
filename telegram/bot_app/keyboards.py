from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

inline_button_USD = InlineKeyboardButton('USD', callback_data='USD')
inline_button_RUB = InlineKeyboardButton('RUB', callback_data='RUB')
inline_button_KZT = InlineKeyboardButton('KZT', callback_data='KZT')
inline_kb = InlineKeyboardMarkup()

inline_kb.add(inline_button_USD)
inline_kb.add(inline_button_RUB)
inline_kb.add(inline_button_KZT)
