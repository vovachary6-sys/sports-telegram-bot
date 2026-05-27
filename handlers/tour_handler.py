from parsers.super_espn_parser import get_tour_matches
from handlers.league_handler import user_league

waiting_for_tour = {}


async def handle_tour_input(update, context):

    user_id = update.message.from_user.id

    if user_id not in waiting_for_tour:
        return False

    text = update.message.text

    if not text.isdigit():

        await update.message.reply_text(
            "Введите номер тура числом."
        )

        return True

    tour = int(text)

    league = user_league.get(user_id)

    result = get_tour_matches(league, tour)

    await update.message.reply_text(result)

    del waiting_for_tour[user_id]

    return True