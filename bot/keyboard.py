from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_keyboard():
    kb = InlineKeyboardMarkup()

    kb.row(
        InlineKeyboardButton("C", callback_data="C"),
        InlineKeyboardButton("⌫", callback_data="BACK"),
        InlineKeyboardButton("+/-", callback_data="NEG"),
        InlineKeyboardButton("^", callback_data="^")
    )

    kb.row(
        InlineKeyboardButton("7", callback_data="7"),
        InlineKeyboardButton("8", callback_data="8"),
        InlineKeyboardButton("9", callback_data="9"),
        InlineKeyboardButton("÷", callback_data="÷")
    )

    kb.row(
        InlineKeyboardButton("4", callback_data="4"),
        InlineKeyboardButton("5", callback_data="5"),
        InlineKeyboardButton("6", callback_data="6"),
        InlineKeyboardButton("×", callback_data="×")
    )

    kb.row(
        InlineKeyboardButton("1", callback_data="1"),
        InlineKeyboardButton("2", callback_data="2"),
        InlineKeyboardButton("3", callback_data="3"),
        InlineKeyboardButton("-", callback_data="-")
    )

    kb.row(
        InlineKeyboardButton("0", callback_data="0"),
        InlineKeyboardButton("(", callback_data="("),
        InlineKeyboardButton(")", callback_data=")"),
        InlineKeyboardButton(",", callback_data=",")
    )

    kb.row(
        InlineKeyboardButton("k", callback_data="k"),
        InlineKeyboardButton("m", callback_data="m"),
        InlineKeyboardButton("b", callback_data="b"),
        InlineKeyboardButton("+", callback_data="+")
    )

    kb.row(
        InlineKeyboardButton("=", callback_data="=")
    )

    return kb