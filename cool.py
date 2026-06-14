import telebot
import os
from simpleeval import simple_eval
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
user_data = {}

def get_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    row1 = [telebot.types.KeyboardButton("7"), telebot.types.KeyboardButton("8"), telebot.types.KeyboardButton("9"), telebot.types.KeyboardButton("÷")]
    row2 = [telebot.types.KeyboardButton("4"), telebot.types.KeyboardButton("5"), telebot.types.KeyboardButton("6"), telebot.types.KeyboardButton("×")]
    row3 = [telebot.types.KeyboardButton("1"), telebot.types.KeyboardButton("2"), telebot.types.KeyboardButton("3"), telebot.types.KeyboardButton("-")]
    row4 = [telebot.types.KeyboardButton("0"), telebot.types.KeyboardButton(","), telebot.types.KeyboardButton("^"), telebot.types.KeyboardButton("="), telebot.types.KeyboardButton("+")]
    keyboard.add(*row1)
    keyboard.add(*row2)
    keyboard.add(*row3)
    keyboard.add(*row4)
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'добро пожаловать на бот калькулятор',reply_markup = get_keyboard())

@bot.message_handler(commands=['calc'])
def calc_command(message):
    bot.send_message(message.chat.id,'пример: 4+7')

@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def calculator(message):
    user_id = message.chat.id
    text = message.text
    if user_id not in user_data:
        user_data[user_id] = ""

    if text in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                "+", "-", "×", "÷", ",", "^"]:
        user_data[user_id] += text
        return

    if text == "=":
        try:
            expr = user_data[user_id]

            expr = expr.replace("×", "*")
            expr = expr.replace("÷", "/")
            expr = expr.replace(",", ".")
            expr = expr.replace("^", "**")

            result = simple_eval(expr)

            bot.send_message(user_id, f"Ответ: {result}")

            user_data[user_id] = ""

        except ZeroDivisionError:
            bot.send_message(
                message.chat.id,
                'Ошибка деления на ноль')

        except Exception:
            bot.send_message(
                message.chat.id,
                "Ошибка"
            )

        return

    try:
        expr = text
        user_data[user_id] = ""
        expr = expr.replace("×", "*")
        expr = expr.replace("÷", "/")
        expr = expr.replace(",", ".")
        expr = expr.replace("^", "**")

        if expr.startswith(","):
            expr = "0" + expr

        result = simple_eval(expr)

        bot.send_message(user_id, f"Ответ: {result}")

    except ZeroDivisionError:
        bot.send_message(user_id, "Ошибка деления на ноль")

    except Exception:
        bot.send_message(user_id, "Ошибка")


bot.polling()