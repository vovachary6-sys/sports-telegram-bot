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
from handlers.world_cup_handler import world_cup_handler


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
        filters.Regex("^🌍 World Cup 2026$"),
        world_cup_handler
    )
)

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            match_type_handler
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()