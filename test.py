import telebot
from config import keys, TOKEN
from extensions import ConversionException, CurrencyConverter


bot = telebot.TeleBot(TOKEN)


keys = {
    'рубль': 'RUB',
    'доллар': 'USD',
    'евро': 'EUR'
}


@bot.message_handler(commands=['start', 'help'])
def help_command(message: telebot.types.Message):
    text = '''Привет! Я бот, который поможет тебе узнать цену на определённое количество валюты.
    Чтобы узнать цену, отправь мне сообщение в следующем формате:
    <имя валюты, цену которой ты хочешь узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>
    Например: доллар рубль 100
    Чтобы узнать возможные валюты отправьте сообщение /values
    '''
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
       text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConversionException(f'Неправильное колличество параметров!')

        base, quote, amount = values
        total_base = CurrencyConverter.convert(base, quote, amount)
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()