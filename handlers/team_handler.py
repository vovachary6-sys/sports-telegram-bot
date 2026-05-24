from telegram import Update

from parsers.super_espn_parser import search_team


async def team_handler(update: Update, context):

    if not context.args:

        await update.message.reply_text(
            "Использование:\n/team Arsenal"
        )

        return

    team_name = " ".join(context.args)

    result = search_team(team_name)

    await update.message.reply_text(result)