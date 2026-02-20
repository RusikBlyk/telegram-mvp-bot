import os
from dotenv import load_dotenv
from telegram.ext import Application

from bot.handlers.start import get_start_handlers
from bot.handlers.flashcards import get_flashcard_handlers
from bot.db.database import init_db

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


def main():
    init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    # --- start handlers ---
    for handler in get_start_handlers():
        app.add_handler(handler)

    # --- flashcard handlers ---
    for handler in get_flashcard_handlers():
        app.add_handler(handler)

    print("🚀 Bot started (polling)")
    app.run_polling()


if __name__ == "__main__":
    main()