import telebot
import os
import re
from dotenv import load_dotenv
from calculator.normalize import normalize
from calculator.engine import calculate
from bot.keyboard import get_keyboard
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
user_data = {}
user_screen = {}

def check_brackets(expr):
    stack = []
    for c in expr:
        if c == "(":
            stack.append(c)
        elif c == ")":
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0

def show_screen(user_id, chat_id):
    expr = user_data.get(user_id, "")
    text = f"🧮 {expr if expr else '0'}"

    if user_id in user_screen:
        old_chat_id, old_msg_id = user_screen[user_id]
        try:
            bot.delete_message(old_chat_id, old_msg_id)
        except:
            pass

    msg = bot.send_message(chat_id, text)

    user_screen[user_id] = (chat_id, msg.message_id)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'добро пожаловать на бот калькулятор введите /calc чтобы открыть клавиатуру калькулятора\nили /help для помощи')

@bot.message_handler(commands=['calc'])
def calc_command(message):
    bot.send_message(message.chat.id,'экранная клавиатура',reply_markup = get_keyboard())

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id,'вы можете начать работу либо с помощью кнопок на экране,\nлибо самостоятельно набрав выражение пример:8+9^6')

@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def calculator(message):
    user_id = message.chat.id
    text = message.text
    if user_id not in user_data:
        user_data[user_id] = ""

    if text == "⌫":
        expr = user_data.get(user_id, "")
        if expr:
            user_data[user_id] = expr[:-1]
        show_screen(user_id, message.chat.id)
        return

    if text == 'C':
        user_data[user_id] = ""
        bot.send_message(message.chat.id, "🧹 очищено")
        show_screen(user_id, message.chat.id)
        return

    if text == "+/-":
        if user_data[user_id]:
            if user_data[user_id].startswith("-"):
                user_data[user_id] = user_data[user_id][1:]
            else:
                user_data[user_id] = "-" + user_data[user_id]
        show_screen(user_id, message.chat.id)
        return

    if text in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                "+", "-", "×", "÷", ",", "^",'k','m','b','(',')']:
        user_data[user_id] += text
        show_screen(user_id, message.chat.id)
        return

    if text == "=":
        try:
            expr = user_data.get(user_id, "")

            if not check_brackets(expr):
                bot.send_message(user_id, "скобки не сбалансированы")
                return
            if not expr:
                bot.send_message(user_id, "Пустое выражение")
                return
            expr = normalize(expr)
            result = calculate(expr)
            bot.send_message(user_id, f"🧮 Ответ: {result}")
            user_data[user_id] = ""
            show_screen(user_id, message.chat.id)

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
        expr = normalize(text)
        if not re.search(r"\d", expr):
            bot.send_message(user_id, "❌ неверное выражение")
            show_screen(user_id, message.chat.id)
            return

        if not check_brackets(expr):
            bot.send_message(user_id, "скобки не сбалансированы")
            return

        user_data[user_id] = ""
        if expr.startswith(","):
            expr = "0" + expr

        result = calculate(expr)

        bot.send_message(user_id, f"🧮 Ответ: {result}")

    except ZeroDivisionError:
        bot.send_message(user_id, "Ошибка деления на ноль")

    except Exception:
        bot.send_message(user_id, "Ошибка")


bot.polling()