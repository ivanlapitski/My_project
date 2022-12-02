from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('start')
b2 = KeyboardButton('categories')
b3 = KeyboardButton('today')
b4 = KeyboardButton('month')
b5 = KeyboardButton('expenses')

button_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

button_client.add(b1).row(b2, b3).row(b4, b5)

