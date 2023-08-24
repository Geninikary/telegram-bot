import telebot

from config import keys, TOKEN
from extensions import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = f"Здравствуйте {message.from_user.first_name}\n \
Для конвертации валюты введите команду боту:\n<наименование валюты>\n \
<в какую валюту перевести>\n \
<количество переводимой валюты: </values>"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def value(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys:
        text = '\n'.join((text, f'<b>{key}</b>'))
    bot.reply_to(message, text, parse_mode='html')


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров')

        quote, base, amount = values
        total_base = CurrencyConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n {e}')

    except BaseException as e:
        bot.reply_to(message, f'Не удалось обработать команду \n {e}')
    else:
        result = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, result)


bot.polling(none_stop=True)
