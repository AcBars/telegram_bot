from random import randint
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot



def pool_print(pool):
    arr = pool.copy()
    for i in range(3):
        arr[i] = ''.join(arr[i])
    bot.send_message(id, ' _ ' * 3)
    bot.send_message(id, '\n'.join(arr))


def step_bot(pool):
    x = randint(0, 2)
    y = randint(0, 2)
    while pool[x][y] == '|X|' or pool[x][y] == '|0|':
        x = randint(0, 2)
        y = randint(0, 2)
    pool[x][y] = '|X|'
    step = 1
    return step


def check_win(pool, step):
    for i in range(3):
        win = pool[i][0] + pool[i][1] + pool[i][2]
        if win == '|X||X||X|':
            bot.send_message(id, 'Выйграл компьютер!')
            step = 2
            return step
    for i in range(3):
        win = pool[0][i] + pool[1][i] + pool[i][i]
        if win == '|X||X||X|':
            bot.send_message(id, 'Выйграл компьютер!')
            step = 2
            return step
    win = pool[0][0] + pool[1][1] + pool[2][2]
    if win == '|X||X||X|':
        bot.send_message(id, 'Выйграл компьютер!')
        step = 2
        return step
    win = pool[0][2] + pool[1][1] + pool[2][0]
    if win == '|X||X||X|':
        bot.send_message(id, 'Выйграл компьютер!')
        step = 2
        return step
    for i in range(3):
        win = pool[i][0] + pool[i][1] + pool[i][2]
        if win == '|0||0||0|':
            bot.send_message(id, 'Поздравляю! Вы выйграли!')
            step = 2
            return step
    for i in range(3):
        win = pool[0][i] + pool[1][i] + pool[2][i]
        if win == '|0||0||0|':
            bot.send_message(id, 'Поздравляю! Вы выйграли!')
            step = 2
            return step
    win = pool[0][0] + pool[1][1] + pool[2][2]
    if win == '|0||0||0|':
        bot.send_message(id, 'Поздравляю! Вы выйграли!')
        step = 2
        return step
    win = pool[0][2] + pool[1][1] + pool[2][0]
    if win == '|0||0||0|':
        bot.send_message(id, 'Поздравляю! Вы выйграли!')
        step = 2
        return step
    return step


def step_human(pool):
    reqvest_move_1()
    x = int(date[0])
    y = int(date[1])
    x -= 1
    y -= 1
    if x < 0 or x > 2 or y < 0 or y > 2:
        bot.send_message(id, 'Выпромахнулись! И не попали в поле. Ход переходит компьютеру.')
    else:
        pool[x][y] = '|0|'
    step = 0
    return step


def end_game(arr, step):
    for i in range(3):
        for j in range(3):
            if arr[i][j] == '|_|':
                return step
    bot.send_message(id, 'Игра завершена. Свободных полей не осталось')
    step = 2
    return step

def start_game():
    pool = []
    for i in range(3):
        pool.append([])
        for j in range(3):
            pool[i].append('|_|')
    step = randint(0, 1)
    if step == 0:
        await bot.send_message(id, 'Первым ходит компьютер.')
        step = step_bot(pool)
        pool_print(pool)
    else:
        await bot.send_message(id, 'Вы ходите первым')
        pool_print(pool)
        step = step_human(pool)
        pool_print(pool)
    while step != 2:
        if step == 0:
            step = step_bot(pool)
            step = check_win(pool, step)
            step = end_game(pool, step)
            pool_print(pool)
        else:
            step = step_human(pool)
            step = check_win(pool, step)
            step = end_game(pool, step)
            pool_print(pool)
id = None
date = None

class FMSAdmin(StatesGroup):
    line = State()
    column = State()

async def crestiki(message: types.Message):
    global id
    id = message.from_user.id
    start_game()

async def reqvest_move_1(message: types.Message, state:FSMContext):
    global date
    await bot.send_message(id, 'Введите строку куда поставить 0: ')
    async with state.proxy() as date:
        date[0] = message.text
    await FMSAdmin.next()
    await bot.send_message(id, 'Введите столбец куда поставить 0: ')

async def reqvest_move_2(message: types.Message, state:FSMContext):
    global date
    async with state.proxy() as date:
        date[1] = message.text
    await state.finish()


def reg_handler_game(dp: Dispatcher):
    dp.register_message_handler(crestiki, commands=['Играть_в_крестики_нолики'])


