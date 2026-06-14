import telebot
from simpleeval import simple_eval
TOKEN = '8563975591:AAHN_OmAo90T3YXIXptCi29eysPIEsgOX2o'
bot = telebot.TeleBot(TOKEN)

def calculate(a, b, oper):
    match oper:
        case '+':
            return a + b
        case '-':
            return a - b
        case '*':
            return a * b
        case '/':
            if b == 0:
                return "Нельзя делить на 0"
            return round(a/b,4)
        case '**':
            return a ** b
        case _:
            return "Неизвестная операция"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'welcome')

@bot.message_handler(commands=['calc'])
def calc(message):
    bot.send_message(message.chat.id,'пример: 4+7')

@bot.message_handler(func=lambda message: True)
def calculator(message):
    try:
        result = simple_eval(message.text)

        bot.send_message(
            message.chat.id,
            f"Ответ: {result}"
        )

    except Exception:
        bot.send_message(
            message.chat.id,
            "Ошибка"
        )
bot.polling()