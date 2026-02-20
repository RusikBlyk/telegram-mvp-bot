import os
from dotenv import load_dotenv
from telegram.ext import Application

from bot.handlers.start import get_start_handlers
from bot.handlers.flashcards import get_flashcard_handler

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # handlers
    for handler in get_start_handlers():
        app.add_handler(handler)

    app.add_handler(get_flashcard_handler())

    print("🚀 Bot started (polling)")
    app.run_polling()


if __name__ == "__main__":
    main()
