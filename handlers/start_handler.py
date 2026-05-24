from telegram import Update
from telegram.ext import ContextTypes

from keyboards.main_keyboard import (
    get_main_keyboard
)


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🏆 Sports Bot",
        reply_markup=get_main_keyboard()
    )