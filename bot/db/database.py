import sqlite3
from pathlib import Path

DB_PATH = Path("bot.db")


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                current_index INTEGER DEFAULT 0
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS known_words (
                user_id INTEGER,
                word TEXT,
                PRIMARY KEY (user_id, word)
            )
        """)

        conn.commit()


def get_user(user_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT current_index FROM users WHERE user_id = ?",
            (user_id,)
        )
        result = cursor.fetchone()

        if result:
            return result[0]

        # якщо користувача ще нема
        cursor.execute(
            "INSERT INTO users (user_id, current_index) VALUES (?, 0)",
            (user_id,)
        )
        conn.commit()
        return 0


def update_index(user_id: int, new_index: int):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET current_index = ? WHERE user_id = ?",
            (new_index, user_id)
        )
        conn.commit()


def add_known_word(user_id: int, word: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO known_words (user_id, word) VALUES (?, ?)",
            (user_id, word)
        )
        conn.commit()


def get_known_words(user_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT word FROM known_words WHERE user_id = ?",
            (user_id,)
        )
        return [row[0] for row in cursor.fetchall()]