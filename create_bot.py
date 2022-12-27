from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

token = input('Введитие API бота: ')
bot = Bot(token)
storage = MemoryStorage()
dp =Dispatcher(bot, storage=storage)