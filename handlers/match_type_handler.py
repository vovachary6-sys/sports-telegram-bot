from telegram import Update

from parsers.super_espn_parser import (
    get_matches,
    LEAGUES
)

from keyboards.main_keyboard import get_main_keyboard
from keyboards.match_type_keyboard import get_match_type_keyboard

from handlers.league_handler import user_league
from handlers.tour_handler import waiting_for_tour


async def match_type_handler(update: Update, context):

    user_id = update.message.from_user.id
    text = update.message.text

    if text == "Выбрать другую лигу":

        if user_id in user_league:
            del user_league[user_id]

        await update.message.reply_text(
            "Выбери лигу:",
            reply_markup=get_main_keyboard()
        )

        return

    if text in LEAGUES:

        user_league[user_id] = text

        await update.message.reply_text(
            f"Лига выбрана: {text}",
            reply_markup=get_match_type_keyboard()
        )

        return

    if user_id not in user_league:

        await update.message.reply_text(
            "Выбери лигу:",
            reply_markup=get_main_keyboard()
        )

        return

    league = user_league[user_id]

    if text == "Недавние матчи":

        result = get_matches(league, "recent")

        await update.message.reply_text(result)

        return

    if text == "Выбери тур":

        waiting_for_tour[user_id] = True

        await update.message.reply_text(
            "Введите номер тура:"
        )

        return

    if text == "Live":

        result = get_matches(league, "live")

        await update.message.reply_text(result)

        return