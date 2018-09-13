import conf
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import ephem
import time


handler = logging.FileHandler(conf.LOG_PATH, 'a', encoding='UTF-8')
handler.setFormatter(
    logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
log = logging.getLogger()
log.addHandler(handler)
log.setLevel(conf.LOG_LEVEL)

default_response = 'Попробуй другую команду.'

def start_message(bot, update):
    user_text = update.message.text
    log.info(f'user_text={user_text}')
    reply_text = 'Привет!'
    log.info(f'reply_text={reply_text}')
    update.message.reply_text(reply_text)

def chat(bot, update):
    log.info(f'user_text={update.message.text}')
    update.message.reply_text(default_response)

def space_talks(bot, update):
    log.info(f'user_text={update.message.text}')
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

if __name__ == '__main__':
    log.info('Bot start')
    bot = Updater(conf.BOT_PRIVATE_KEY, request_kwargs=conf.PROXY)
    dp = bot.dispatcher
    dp.add_handler(CommandHandler('start', start_message))
    dp.add_handler(CommandHandler('planet', space_talks))
    dp.add_handler(MessageHandler(Filters.text, chat))
    bot.start_polling()
    bot.idle()
