import random

from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes
from telegram.ext import MessageHandler
from telegram.ext import filters
from bot.data.words import WORDS
from bot.db.database import (
    get_user,
    update_index,
    add_known_word
)


async def know_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    current_index = get_user(user_id)

    if current_index >= len(WORDS):
        await query.message.answer("🎉 Ти вже знаєш усі слова!")
        return

    card = WORDS[current_index]
    word = card["word"]

    add_known_word(user_id, word)

    new_index = current_index + 1
    update_index(user_id, new_index)

    await send_next_word(query.message, user_id)

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

async def send_next_word(message, user_id):
    index = get_user(user_id)

    if index >= len(WORDS):
        await message.answer("🎉 Ти пройшов усі слова!")
        return

    word = WORDS[index]

    text = (
        f"🇬🇧 {word['word']}\n"
        f"{word['ipa']}\n"
        f"🇺🇦 {word['ua']}"
    )

    await message.answer(
        text,
        reply_markup=build_keyboard()
    )


# 🔥 ГОЛОВНИЙ handler кнопок
async def flashcard_buttons(update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # показуємо наступну картку
    await send_flashcard(query.message.chat_id, context)


def get_flashcard_handlers():
    return [
        CallbackQueryHandler(know_word, pattern="^know$"),
        CallbackQueryHandler(flashcard_buttons, pattern="^(dont_know|next)$"),
    ]
