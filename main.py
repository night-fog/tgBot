from __future__ import division

import conf
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import logging
import ephem
import time
import re
from cities_game import CitiesGame
from os.path import dirname, realpath


handler = logging.FileHandler(conf.LOG_PATH, 'a', encoding='UTF-8')
handler.setFormatter(
    logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
log = logging.getLogger()
log.addHandler(handler)
log.setLevel(conf.LOG_LEVEL)

default_response = 'Попробуй другую команду.'

math_operators = {
    '+': '__add__',
    '-': '__sub__',
    '*': '__mul__',
    '/': '__truediv__'
}

calc_keyboard = [
    ['1', '2', '3', '+'],
    ['4', '5', '6', '-'],
    ['7', '8', '9', '*'],
    ['-', '0', '=', '/']
]
calc_reply_markup = ReplyKeyboardMarkup(calc_keyboard)

global data
data = str()
global cities
cities_file = '{}/res/cities.txt'
path = dirname(realpath(__file__))
cities = CitiesGame(cities_file.format(path))

def math_count(input_text: str):
    re_main_math = '^([0-9,\-]{1,})([+,\-,/,*]{1})([0-9,\-]{1,})=$'
    data_found_list = re.findall(re_main_math, input_text)
    if not isinstance(data_found_list, list) or len(data_found_list) != 1:
        return False
    elements = re.search(re_main_math, input_text)
    first_number = int(elements.group(1))
    operator = math_operators.get(elements.group(2))
    second_number = int(elements.group(3))
    try:
        result = eval(f'first_number.{operator}(second_number)')
    except SyntaxError:
        return False
    except ZeroDivisionError:
        return 'Делить на ноль недопустимо в этой Вселенной.'
    if not isinstance(result, int) and not isinstance(result, float):
        return False
    return result


def start_message(bot, update):
    user_text = update.message.text
    log.info(f'start_message:user_text={user_text}')
    reply_text = 'Привет!'
    log.info(f'reply_text={reply_text}')
    update.message.reply_text(reply_text)

def chat(bot, update):
    input_text = update.message.text.strip()
    log.info(f'chat:user_text={input_text}')
    response = math_count(input_text)
    if response is not False:
        update.message.reply_text(response)
    else:
        update.message.reply_text(default_response)

def space_talks(bot, update):
    log.info(f'space_talks:user_text={update.message.text}')
    input_list = update.message.text.split()
    if len(input_list) < 2:
        update.message.reply_text(
            'Попробуй ввести /planet <Название планеты (на английском)>')
    else:
        planet = input_list[1].capitalize()
        try:
            planet_obj = getattr(ephem, planet)(time.strftime('%Y/%m/%d'))
        except AttributeError:
            update.message.reply_text('Такой планеты не знаю, дружок, извини!')
        else:
            constellation_name = ephem.constellation(planet_obj)
            update.message.reply_text(
                'Сегодня она будет в созвездии {}, {}'.format(constellation_name[0], constellation_name[1]))

def words_count(bot, update):
    input_data = update.message.text
    log.info(f'words_count:user_text={input_data}')
    data_found_list = re.findall('"([a-zA-Zа-яА-Я\s-]{1,})"', input_data)
    if len(data_found_list) == 0:
        update.message.reply_text('В введенной строке нет слов в двойных кавычках.')
    else:
        print(len(data_found_list))
        reply = ''
        for data_found in data_found_list:
            data_len = len(data_found.strip().split())
            #  @ToDo: добавить склонение слова "слов"
            reply += f'Во фразе "{data_found}" {data_len} слов.\n'
        update.message.reply_text(reply)

def math_calc_count(bot, update):
    input_data = update.message.text
    log.info(f'math_calc_count:user_text={input_data}')
    #while update.message.text != '=':
    bot.send_message(chat_id=update.message.chat_id, text='Введите следующий символ или "=" для вычисления', reply_markup=calc_reply_markup)
    data += update.message.text
    update.message.reply_text(data)

def cities_game(bot, update):
    input_data = update.message.text
    log.info(f'cities_game:user_text={input_data}')
    letter = input_data.strip()[-1].lower()
    if not re.match('[а-я]', letter):
        update.message.reply_text('Введи лучше русский город')
    resp_city = cities.get(letter)
    if resp_city is False or resp_city is None:
        cities.read_cities()
        update.message.reply_text('Не помню больше русских городов, роботы проиграли, но только в этот раз.')
    else:
        update.message.reply_text(resp_city)

if __name__ == '__main__':
    log.info('Bot start')
    bot = Updater(conf.BOT_PRIVATE_KEY, request_kwargs=conf.PROXY)
    dp = bot.dispatcher
    dp.add_handler(CommandHandler('start', start_message))
    dp.add_handler(CommandHandler('planet', space_talks))
    dp.add_handler(CommandHandler('wordcount', words_count))
    dp.add_handler(CommandHandler('goroda', cities_game))
    dp.add_handler(CommandHandler('math', math_calc_count))
    dp.add_handler(MessageHandler(Filters.text, chat))
    bot.start_polling()
    bot.idle()
