import conf
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

handler = logging.FileHandler(conf.LOG_PATH, 'a', encoding='UTF-8')
handler.setFormatter(
    logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
log = logging.getLogger()
log.addHandler(handler)
log.setLevel(conf.LOG_LEVEL)

def start_message(bot, update):
    user_text = update.message.text
    log.info(f'user_text={user_text}')
    reply_text = 'Привет!'
    log.info(f'reply_text={reply_text}')
    update.message.reply_text(reply_text)

def chat(bot, update):
    user_text = update.message.text
    log.info(f'user_text={user_text}')
    reply_text = user_text
    log.info(f'reply_text={reply_text}')
    update.message.reply_text(user_text)

if __name__ == '__main__':
    log.info('Bot start')
    bot = Updater(conf.BOT_PRIVATE_KEY, request_kwargs=conf.PROXY)
    dp = bot.dispatcher
    dp.add_handler(CommandHandler('start', start_message))
    dp.add_handler(MessageHandler(Filters.text, chat))
    bot.start_polling()
    bot.idle()
