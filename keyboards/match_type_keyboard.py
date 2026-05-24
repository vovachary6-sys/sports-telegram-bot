from telegram import ReplyKeyboardMarkup


def get_match_type_keyboard():

    keyboard = [

        ["Завершенные", "Live"],

        ["Предстоящие"],

        ["Выбрать другую лигу"]

    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )