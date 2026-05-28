from telegram import Update

from parsers.super_espn_parser import search_team


MAX_MESSAGE_LENGTH = 4000


async def send_long_message(message, text):

    for i in range(0, len(text), MAX_MESSAGE_LENGTH):

        chunk = text[i:i + MAX_MESSAGE_LENGTH]

        await message.reply_text(chunk)


async def team_handler(update: Update, context):

    if not context.args:

        await update.message.reply_text(
            "Использование:\n/team Arsenal"
        )

        return

    team_name = " ".join(context.args)

    result = search_team(team_name)

    await send_long_message(update.message, result)