from telegram import ReplyKeyboardMarkup


def get_leagues_keyboard():

    keyboard = [

        ["Premier League", "La Liga"],
        ["Bundesliga", "Serie A"],
        ["Ligue 1", "Championship"],

        ["Eredivisie", "Liga Portugal"],
        ["Saudi Pro League"],

        ["UEFA Champions League", "UEFA Europa League"],

        ["NBA", "NHL"]

    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )