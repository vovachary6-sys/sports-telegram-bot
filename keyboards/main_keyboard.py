from telegram import ReplyKeyboardMarkup

def get_main_keyboard():

    keyboard = [

        ["NBA", "NHL"],

        ["Premier League", "Championship"],

        ["La Liga", "Bundesliga"],

        ["Serie A", "Ligue 1"],

        ["Eredivisie", "Liga Portugal"],

        ["Saudi Pro League"],

        ["UEFA Champions League", "UEFA Europa League"],
        ["🌍World Cup 2026"]

    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )