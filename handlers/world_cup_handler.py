from telegram import Update
from telegram.ext import ContextTypes


async def world_cup_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = (
        "🌍 World Cup 2026\n\n"
        "Функция скоро будет готова 🚀"
    )

    await update.message.reply_text(text)