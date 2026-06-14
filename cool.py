import telebot
import os
from simpleeval import simple_eval
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'добро пожаловать на бот калькулятор')

@bot.message_handler(commands=['calc'])
def calc(message):
    bot.send_message(message.chat.id,'пример: 4+7')

@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def calculator(message):
    try:
        text = message.text
        text = text.replace("×", "*")
        text = text.replace("÷", "/")
        text = text.replace("^", "**")

        result = simple_eval(text)

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