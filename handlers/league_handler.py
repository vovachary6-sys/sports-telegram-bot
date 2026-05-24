from telegram import Update

from keyboards.match_type_keyboard import get_match_type_keyboard

user_league = {}


async def league_handler(update: Update, context):

    league = update.message.text
    user_id = update.message.from_user.id

    user_league[user_id] = league

    await update.message.reply_text(
        f"Лига: {league}\n\nВыберите тип матчей:",
        reply_markup=get_match_type_keyboard()
    )