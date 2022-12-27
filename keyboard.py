from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start =KeyboardButton('/start')
b1 = KeyboardButton('/Играть_в_крестики_нолики')
b2 = KeyboardButton('/Калькулятор')

keyboards = ReplyKeyboardMarkup(resize_keyboard=True)
keyboards.add(start).row(b1, b2)