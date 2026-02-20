import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes
from bot.data.words import WORDS


def build_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("✅ Знаю", callback_data="know"),
            InlineKeyboardButton("🔁 Не знаю", callback_data="dont_know"),
        ],
        [
            InlineKeyboardButton("➡️ Далі", callback_data="next"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


async def send_flashcard(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    word = random.choice(WORDS)

    text = (
        f"🇬🇧 {word['word']}\n"
        f"{word['ipa']}\n"
        f"🇺🇦 {word['ua']}"
    )

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=word["image"],
        caption=text,
        reply_markup=build_keyboard(),
    )


# 🔥 ГОЛОВНИЙ handler кнопок
async def flashcard_buttons(update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # показуємо наступну картку
    await send_flashcard(query.message.chat_id, context)


def get_flashcard_handler():
    return CallbackQueryHandler(
        flashcard_buttons,
        pattern="^(know|dont_know|next)$",
    )
