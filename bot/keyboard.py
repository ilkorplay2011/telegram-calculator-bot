import telebot

def get_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    row1 = [telebot.types.KeyboardButton("C"), telebot.types.KeyboardButton("7"), telebot.types.KeyboardButton("8"), telebot.types.KeyboardButton("9"), telebot.types.KeyboardButton("÷"), telebot.types.KeyboardButton("("), telebot.types.KeyboardButton(")")]
    row2 = [telebot.types.KeyboardButton("4"), telebot.types.KeyboardButton("5"), telebot.types.KeyboardButton("6"), telebot.types.KeyboardButton("×"), telebot.types.KeyboardButton("k"), telebot.types.KeyboardButton("⌫")]
    row3 = [telebot.types.KeyboardButton("1"), telebot.types.KeyboardButton("2"), telebot.types.KeyboardButton("3"), telebot.types.KeyboardButton("-"), telebot.types.KeyboardButton("m"), telebot.types.KeyboardButton("+/-")]
    row4 = [telebot.types.KeyboardButton("0"), telebot.types.KeyboardButton(","), telebot.types.KeyboardButton("^"), telebot.types.KeyboardButton("="), telebot.types.KeyboardButton("+"),telebot.types.KeyboardButton("b")]
    keyboard.add(*row1)
    keyboard.add(*row2)
    keyboard.add(*row3)
    keyboard.add(*row4)
    return keyboard