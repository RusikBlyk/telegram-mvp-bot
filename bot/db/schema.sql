-- Users table: stores user progress
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    current_index INTEGER DEFAULT 0
);

-- Known words table: tracks words user already knows
CREATE TABLE IF NOT EXISTS known_words (
    user_id INTEGER,
    word TEXT,
    PRIMARY KEY (user_id, word),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
