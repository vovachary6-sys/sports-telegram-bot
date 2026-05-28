from telegram import ReplyKeyboardMarkup


def get_match_type_keyboard():

    keyboard = [

        ["Недавние матчи"],

        ["Выбери тур"],

        ["Live"],

        ["Выбрать другую лигу"]

    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )