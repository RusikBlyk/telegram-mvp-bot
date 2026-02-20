from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from bot.handlers.flashcards import send_flashcard



def start_keyboard():
    keyboard = [
        [InlineKeyboardButton("🚀 Почати", callback_data="start_learning")]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт 👋\nГотовий вчити англійські слова?",
        reply_markup=start_keyboard(),
    )


async def start_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await send_flashcard(query.message.chat_id, context)


def get_start_handlers():
    return [
        CommandHandler("start", start_command),
        CallbackQueryHandler(start_button, pattern="^start_learning$"),
    ]

