import sqlite3
from pathlib import Path

DB_PATH = Path("bot.db")
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def init_db():
    """Initialize database with schema from schema.sql"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Read and execute schema
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema = f.read()
            cursor.executescript(schema)
        
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


def get_user_index(user_id: int) -> int:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT current_index FROM users WHERE user_id = ?",
            (user_id,),
        )
        row = cursor.fetchone()

        if row is None:
            cursor.execute(
                "INSERT INTO users (user_id, current_index) VALUES (?, 0)",
                (user_id,),
            )
            conn.commit()
            return 0

        return row[0]


def set_user_index(user_id: int, index: int):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET current_index = ? WHERE user_id = ?",
            (index, user_id),
        )
        conn.commit()