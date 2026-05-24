from telegram import Update
from telegram.ext import ContextTypes

from parsers.world_cup_2026 import (
    get_world_cup_matches
)


async def world_cup_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    matches = await get_world_cup_matches()

    text = "🌍 WORLD CUP 2026\n\n"

    for m in matches:

        text += (
            f"🏆 {m['home']} vs {m['away']}\n"
            f"📊 {m['home_score']}:{m['away_score']}\n"
            f"📍 {m['venue']}\n"
            f"📌 {m['status']}\n"
            f"🕒 {m['time']}\n\n"
            f"📺 {m['link']}\n\n"
        )

    await update.message.reply_text(text)