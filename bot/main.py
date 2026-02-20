import os
import logging
from dotenv import load_dotenv
from telegram.ext import Application, ApplicationBuilder

from bot.handlers.start import get_start_handlers
from bot.handlers.flashcards import get_flashcard_handlers
from bot.db.database import init_db

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def error_handler(update, context):
    """Log the error and notify the user"""
    logger.error(f"Update {update} caused error {context.error}")


def main():
    init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    # --- start handlers ---
    for handler in get_start_handlers():
        app.add_handler(handler)

    # --- flashcard handlers ---
    for handler in get_flashcard_handlers():
        app.add_handler(handler)

    # Add error handler
    app.add_error_handler(error_handler)

    print("🚀 Bot started (polling)")
    logger.info("Bot started successfully")
    app.run_polling(allowed_updates=None)


if __name__ == "__main__":
    main()