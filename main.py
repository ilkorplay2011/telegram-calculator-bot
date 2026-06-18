import telebot
import os
from dotenv import load_dotenv
from bot.keyboard import get_keyboard
from calculator.engine import prepare
from calculator.engine import calculate
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
user_data = {}
user_screen = {}

def show_screen(user_id, chat_id):
    text = user_data.get(user_id, "") or "0"

    # удаляем старый экран
    if user_id in user_screen:
        old_chat_id, old_msg_id = user_screen[user_id]
        try:
            bot.delete_message(old_chat_id, old_msg_id)
        except:
            pass

    # создаём новый экран
    msg = bot.send_message(
        chat_id,
        f"🧮 {text}",
        reply_markup=get_keyboard()
    )

    user_screen[user_id] = (chat_id, msg.message_id)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'добро пожаловать на бот калькулятор введите /calc чтобы открыть клавиатуру калькулятора\nили /help для помощи')

@bot.message_handler(commands=['calc'])
def calc_command(message):
    bot.send_message(message.chat.id,'экранная клавиатура',reply_markup = get_keyboard())

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id,'вы можете начать работу с помощью кнопок на экране введя комманду /calc')

@bot.callback_query_handler(func=lambda call: True)
def handler(call):
    user_id = call.message.chat.id
    data = call.data

    if user_id not in user_data:
        user_data[user_id] = ""

    expr = user_data[user_id]

    if data == "C":
        user_data[user_id] = ""
        show_screen(user_id, user_id)
        return

    if data == "BACK":
        user_data[user_id] = expr[:-1]
        show_screen(user_id, user_id)
        return

    if data == "=":
        try:
            expr = prepare(expr)

            if not expr:
                bot.send_message(user_id, "❌ ошибка")
                return

            result = calculate(expr)

            bot.send_message(user_id, f"🧮 {result}")

            user_data[user_id] = ""
            show_screen(user_id, user_id)

        except Exception:
            bot.send_message(user_id, "❌ ошибка")

        return

    user_data[user_id] += data
    show_screen(user_id, user_id)

bot.infinity_polling()