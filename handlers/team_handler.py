from telegram import Update


async def team_handler(update: Update, context):

    await update.message.reply_text("TEAM WORKS")