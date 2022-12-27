from aiogram import types, Dispatcher
from create_bot import bot
from keyboard import keyboards

async def start_commads(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f'Привет {message.from_user.first_name}!\nЯ умею играть в крестики нолики и считать, как калькулятор',
                           reply_markup=keyboards)





def reg_handler(dp: Dispatcher):
    dp.register_message_handler(start_commads, commands=['start'])

