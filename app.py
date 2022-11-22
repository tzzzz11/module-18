import telebot
from config import TOKEN, keys
from utils import ExchangeException, Exchange

#        MiExchange_bot                Имя бота в Телеграм
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Добро пожаловать в конвертер криптовалют.  \n- Показать список доступных - /values \
    \n- Введите команду в формате <валюта> <в какую валюту перевести> <количество переводимой валюты>\n \
- Помощь - /help'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Введите команду в формате <валюта> <в какую валюту перевести> <количество переводимой валюты> \
            \nили команду /values для списка доступных валют'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ExchangeException('В запросе должно быть три параметра')
        quote, base, amount = values
        total_base = Exchange.get_price(base, quote, amount)
    except ExchangeException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так с {e}')
    else:
        text = f'Курс {amount} {quote} составляет {total_base} {base}'
        bot.send_message(message.chat.id, text)

bot.polling()
