from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters
)

from config import TOKEN

from handlers.start_handler import start
from handlers.match_type_handler import match_type_handler
from handlers.team_handler import team_handler
from handlers.tour_handler import handle_tour_input


async def handle_all_messages(update, context):

    handled = await handle_tour_input(update, context)

    if handled:
        return

    await match_type_handler(update, context)


def main():

    print("Bot running...")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("team", team_handler)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_all_messages
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()