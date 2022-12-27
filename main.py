from aiogram.utils import executor
from create_bot import dp

import calculator
import interface
import game


async def on_startup(_):
    print('Бот вышел в онлайн.')

interface.reg_handler(dp)
calculator.reg_handler_calc(dp)
game.reg_handler_game(dp)




executor.start_polling(dp, skip_updates = True, on_startup=on_startup)