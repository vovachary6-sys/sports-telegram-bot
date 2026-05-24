from telegram import Update

from keyboards.leagues_keyboard import get_leagues_keyboard


async def start(update: Update, context):

    await update.message.reply_text(
        "Выбери лигу:",
        reply_markup=get_leagues_keyboard()
    )