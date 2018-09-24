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
import inspect

class Bot:
    __log = logging.getLogger()
    __bot = Updater(conf.BOT_PRIVATE_KEY, request_kwargs=conf.PROXY)
    __db = None
    __mode = None
    __cities = None

    default_response = 'Попробуй другую команду.\n Напиши /start, если запутался.'
    __math_operators = {
        '+': '__add__',
        '-': '__sub__',
        '*': '__mul__',
        '/': '__truediv__'
    }
    __mode_list = {
        None,
        'goroda'
    }

    def __init__(self):
        self.__start()

    def __start(self):
        self.__init_log()
        self.__init_dispatcher()
        self.__init_cities_game()
        self.__bot.start_polling()
        self.__bot.idle()

    def __init_log(self):
        handler = logging.FileHandler(conf.LOG_PATH, 'a', encoding='UTF-8')
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.__log.addHandler(handler)
        self.__log.setLevel(conf.LOG_LEVEL)

    def log(self, message, function_name=None):
        if not function_name:
            function_name = inspect.stack()[0][3]
        self.__log.info('{}:{}'.format(function_name, str(message).replace('\n', '\\n')))

    def __init_dispatcher(self):
        self.__dp = self.__bot.dispatcher
        self.__dp.add_handler(CommandHandler('start', self.cmd_start))
        self.__dp.add_handler(CommandHandler('planet', self.cmd_planet))
        self.__dp.add_handler(CommandHandler('wordcount', self.cmd_wordcount))
        self.__dp.add_handler(CommandHandler('math', self.cmd_math))
        self.__dp.add_handler(CommandHandler('goroda', self.cmd_goroda))
        self.__dp.add_handler(MessageHandler(Filters.text, self.main_tread))

    def get_input(self, update, function_name=None, return_command_name=False):
        if not function_name:
            function_name = inspect.stack()[0][3]
        self.log(update.message.text, function_name + ':in')
        if update.message.text[0] == '/':
            data_idx = update.message.text.find(' ')
            if data_idx == -1:
                return False
            data = update.message.text[data_idx:].lstrip()
        else:
            data = update.message.text
        if return_command_name:
            return (update.message.text[1:data_idx], data)
        else:
            return data

    def send_reply(self, message, update, function_name=None):
        if not function_name:
            function_name = inspect.stack()[0][3]
        self.log(message, function_name + ':out')
        update.message.reply_text(message)
        return True

    def send_wrong_command_reply(self, update, function_name=None):
        if not function_name:
            function_name = inspect.stack()[0][3]
        message = f'"{update.message.text}" - Тут что-то не так. Не надо так.'
        self.send_reply(message, update, function_name)

    def set_mode(self, mode=None):
        if mode in self.__mode_list:
            self.__mode = mode
            return True
        else:
            return False

    def get_mode(self):
        return self.__mode

    def main_tread(self, bot, update):
        input_text = self.get_input(update)
        if input_text is False:
            self.send_wrong_command_reply(update)
            return False
        mode = self.get_mode()
        if mode is None:
            reply_text = self.default_response
            self.send_reply(reply_text, update)
            return True
        elif 'goroda' == mode:
            return self.cities_game(input_text, update)

    def cmd_start(self, bot, update):
        #input_text = self.get_input(update)
        reply_text = 'Привет!\n' + \
        'Какие есть команды:\n' + \
        '/start - этот вот вывод\n' + \
        '/planet <planetName> - в каком созвездии сегодня будет планета planetName (название планеты принимается только на английском)\n' + \
        '/wordcount "текст в двойных кавычках" - считает сколько слов в двойных кавычках\n' + \
        '/math <1+2=> - математическое выражение, простой калькулятор\n' + \
        '/goroda <Город России> - игра в города\n'
        self.send_reply(reply_text, update)

    def cmd_planet(self, bot, update):
        self.set_mode(None)
        input_text = self.get_input(update)
        if input_text is False:
            self.send_wrong_command_reply(update)
            return False

        planet = input_text.capitalize()
        try:
            planet_obj = getattr(ephem, planet)(time.strftime('%Y/%m/%d'))
        except AttributeError:
            self.send_reply('Такой планеты не знаю, дружок, извини!', update)
            return False
        else:
            constellation_name = ephem.constellation(planet_obj)
            reply_text = 'Сегодня она будет в созвездии {}, {}'.format(
                constellation_name[0], constellation_name[1])
            self.send_reply(reply_text, update)
            return True

    def cmd_wordcount(self, bot, update):
        self.set_mode(None)
        input_text = self.get_input(update)
        if input_text is False:
            self.send_wrong_command_reply(update)
            return False
        data_found_list = re.findall('"([a-zA-Zа-яА-Я\s-]{1,})"', input_text)
        if len(data_found_list) == 0:
            self.send_reply('В введенной строке нет слов в двойных кавычках.',
                            update)
            return False

        reply_text = ''
        for data_found in data_found_list:
            data_len = len(data_found.strip().split())
            #  @ToDo: добавить склонение слова "слов"
            reply_text += f'Во фразе "{data_found}" {data_len} слов.\n'
        self.send_reply(reply_text, update)

    def cmd_math(self, bot, update):
        self.set_mode(None)
        input_text = self.get_input(update)
        if input_text is False:
            self.send_wrong_command_reply(update)
            return False
        re_main_math = '^([0-9,\-]{1,})([+,\-,/,*]{1})([0-9,\-]{1,})=$'
        data_found_list = re.findall(re_main_math, input_text)
        if not isinstance(data_found_list, list) or len(data_found_list) != 1:
            self.send_wrong_command_reply(update)
            return False
        elements = re.search(re_main_math, input_text)
        first_number = int(elements.group(1))
        operator = self.__math_operators.get(elements.group(2))
        second_number = int(elements.group(3))
        try:
            result = eval(f'first_number.{operator}(second_number)')
        except SyntaxError:
            reply_text = 'Математика не понимает вашего выражения.'
            self.send_reply(reply_text, update)
            return False
        except ZeroDivisionError:
            reply_text = 'Делить на ноль недопустимо в этой Вселенной.'
            self.send_reply(reply_text, update)
            return False
        if not isinstance(result, int) and not isinstance(result, float):
            reply_text = 'Ответ не похож на цифру. Он больше похож на это: {}'.format(
                str(result))
            self.send_reply(reply_text, update)
            return False
        self.send_reply(result, update)
        return True

    def cmd_goroda(self, bot, update):
        self.set_mode('goroda')
        return self.main_tread(bot, update)

    def __init_cities_game(self):
        if self.__cities is None:
            path = dirname(realpath(__file__))
            self.__cities = CitiesGame(conf.CITIES_FILE_PATH.format(path))

    def __cities_game_reset(self):
        self.__cities.read_cities()
        self.set_mode(None)

    def cities_game(self, city, update):
        if not re.match('^[а-я\s-]{1,}$', city.strip().lower()):
            self.send_reply('Введи, лучше, русский город, пожалуйста.', update)
            return False

        first_letter = self.__cities.get_letter()
        if first_letter and city[0].lower() != first_letter:
            reply_text = f'Город должен начинаться на "{first_letter}"'
            self.send_reply(reply_text, update)
            return False

        if self.__cities.is_used(city):
            reply_text = 'Такой город уже был!'
            self.send_reply(reply_text, update)
            return False

        if not self.__cities.has_city(city):
            reply_text = 'Не знаю такого русского города. Давай, подумай еще, ты сможешь.'
            self.send_reply(reply_text, update)
            return False

        self.__cities.delete(city)
        resp = self.__cities.get(city[-1])
        if resp is None:
            reply_text = f'Здорово!\nНе помню больше русских городов на "{city[-1]}".\nРоботы проиграли, но только в этот раз.'
            self.send_reply(reply_text, update)
            self.__cities_game_reset()
            return True

        reply_text = f'{resp}, тебе на {resp[-1]}.'
        self.send_reply(reply_text, update)
        return True
