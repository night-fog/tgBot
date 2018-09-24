import logging


BOT_PRIVATE_KEY = '<telegram bot code>'
PROXY = {
    'proxy_url': 'socks5://<proxy host>:<proxy port>',
    'urllib3_proxy_kwargs':
    {
        'username': '<proxy login>',
        'password': '<proxy password>'
    }
}
LOG_PATH = 'bot.log'
LOG_LEVEL = logging.INFO
CITIES_FILE_PATH = '{}/res/cities.txt'
