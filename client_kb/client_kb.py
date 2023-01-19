from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


cancel_button = KeyboardButton('cancel')

cancel_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
).add(
    KeyboardButton('cancel')
)






