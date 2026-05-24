from telegram import Update
from keyboards.main_keyboard import get_main_keyboard


async def start(update: Update, context):
    await update.message.reply_text(
        "🏀⚽ Выбери лигу:",
        reply_markup=get_main_keyboard()
    )