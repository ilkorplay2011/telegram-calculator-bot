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

    if data not in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                    "+", "-", "×", "÷", "^", "(", ")", ",", "k", "m", "b",
                    "=", "C", "BACK", "NEG"}:
        return

    if user_id not in user_data:
        user_data[user_id] = ""

    expr = user_data[user_id]

    if data == "C":
        user_data[user_id] = ""
        show_screen(user_id, call.message.chat.id)
        return

    if data == "BACK":
        user_data[user_id] = expr[:-1]
        show_screen(user_id, call.message.chat.id)
        return

    if data == "NEG":
        if user_data[user_id].startswith("-"):
            user_data[user_id] = user_data[user_id][1:]
        else:
            user_data[user_id] = "-" + user_data[user_id]
        show_screen(user_id, call.message.chat.id)
        return

    if data == "=":
        try:
            if not user_data[user_id]:
                bot.send_message(user_id, "❌ пустое выражение")
                return

            expr = prepare(user_data[user_id])

            if not expr:
                bot.send_message(user_id, "❌ ошибка выражения")
                return

            result = calculate(expr)

            bot.send_message(user_id, f"🧮 {result}")
            user_data[user_id] = ""
            show_screen(user_id, call.message.chat.id)

        except ZeroDivisionError:
            bot.send_message(user_id,'Ошибка деления на ноль')

        except Exception:
            bot.send_message(user_id, "❌ ошибка")


        return

    user_data[user_id] += data
    show_screen(user_id, call.message.chat.id)

bot.infinity_polling()