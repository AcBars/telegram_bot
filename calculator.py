from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
import re



def percentage(full_expression):
    pattern = re.compile(r"[-+]?[\.0-9]+%?")
    m = pattern.findall(full_expression)
    sum = float(0)
    if m:
        sum = float(str(m[0]))
        for i in range(1, len(m)):
            if str(m[i]).find('%') > 0:
                if i != 0:
                    f = float(str(m[i]).rstrip('%'))
                    p = float(m[i - 1])
                    sum += p * f / 100
                    return str(sum)
                else:
                    print('неотчего брать процент')
                    return 'NaN'
            sum += float(str(m[i]))
    else:
        ret = 'NaN'


def prepare_expression(expression):
    full_expression = expression.replace(" ", '')
    full_expression = full_expression.replace(",", '.')
    ''' проверка, три pyака подряд - ошибка '''
    pattern = re.compile(r"[-+*\/]{3,}")
    m = pattern.findall(full_expression)
    if m:
        return 'NaN'
    ''' конец проверки '''
    return full_expression


def calculation(full_expression):
    full_expression = prepare_expression(full_expression)
    pattern = re.compile(r"\([-+ *\/.\d\s]+\)")
    m = pattern.search(full_expression)
    if not m:
        # print(':'+full_expression)
        full_expression = calculate_mul_div(full_expression)
        return full_expression

    while m:
        # print(f'full_expression[m.start():m.end()]: {full_expression[m.start():m.end()]}')
        value = calculate_mul_div(full_expression[m.start():m.end()])
        # print(value)
        if float(value) > 0:
            full_expression = full_expression[:m.start()] + "+" + value + full_expression[m.end():]
        else:
            full_expression = full_expression[:m.start()] + value + full_expression[m.end():]
        # print(full_expression)
        m = pattern.search(full_expression)
        # addition
        # full_expression = calculate_mul_div(full_expression)
    return full_expression


def check_val_and_make_exp(full_expression, m, value):
    if float(value) > 0:
        full_expression = full_expression[:m.start()] + "+" + str(value) + full_expression[m.end():]
    else:
        full_expression = full_expression[:m.start()] + str(value) + full_expression[m.end():]
    # print(f' check_val_and_make_exp Return Value:\t\t {full_expression}')
    return full_expression


def calculate_mul_div(full_expression):
    full_expression = full_expression.replace(")", '')
    full_expression = full_expression.replace("(", '')

    m = re.search(r'[-+ *\ /][*\ /]', full_expression)
    if m:
        print('Недопустимая компбинация операций')
        return 'NaN'

    # pattern = 'r[-+]?[0-9.]+[*\/][-+]?[0-9.]+'
    m = re.search(r"[-+]?[0-9.]+[*\/][-+]?[0-9.]+", full_expression)
    # dividing
    while m:
        mm = re.search(r'/', m[0])
        # print(f'/m:{m}')
        # print(f'/mm= {mm}')
        if mm:
            d = full_expression[m.start():m.end()]
            # print(d)
            if (d[mm.end():]) != '0':
                value = float(d[:mm.start()]) / float(d[mm.end():])
                full_expression = check_val_and_make_exp(full_expression, m, value)
            else:
                print('ошибка = деление на ноль')
                return 'NaN'

        m = re.search(r"[-+]?[0-9.]+[*\/][-+]?[0-9.]+", full_expression)
        # multiplication
        if m:
            mm = re.search(r'\*', m[0])
            # print(f'*m:{m}')
            # print(f'*mm= {mm}')
            if mm:
                d = full_expression[m.start():m.end()]
                # print(d)
                value = float(d[:mm.start()]) * float(d[mm.end():])
                full_expression = check_val_and_make_exp(full_expression, m, value)
    # addition
    full_expression = calculate_sum_sub(full_expression)
    return full_expression


def calculate_sum_sub(full_expression):
    m = re.findall(r"[-+]?[0-9.]+", full_expression)
    if m:
        s = m.copy()
    else:
        return full_expression
    # addition
    value = 0
    for i in s:
        value += float(i)
    return str(value)


def main_calculation(full_expression):
    full_expression = prepare_expression(full_expression)
    mm = re.search(r'^[-+]?[0-9.]+$', full_expression)
    while not mm:
        full_expression = calculation(full_expression)
        mm = re.search(r'^[-+]?[0-9.]+$', full_expression)
    return full_expression



class FMSAdmin(StatesGroup):
    condition =State()

async def calculator(message: types.Message):
    await FMSAdmin.condition.set()
    await bot.send_message(message.from_user.id, 'Введите выражение которое хотите посчитать: ')

async def load_condition(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['condition'] = message.text
    await bot.send_message(message.from_user.id, f"{str(data['condition'])}={main_calculation(data['condition'])}")
    await state.finish()


# expression = '40/(2 * (2*10-5) + (10*(6-5)) ))'
#
# result = main_calculation(expression)
# print(f'{expression}={result}')



def reg_handler_calc(dp: Dispatcher):
    dp.register_message_handler(calculator, commands=['Калькулятор'])
    dp.register_message_handler(load_condition, state=FMSAdmin.condition)