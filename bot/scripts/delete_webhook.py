from dotenv import load_dotenv
import os
from telegram import Bot


def main():
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("BOT_TOKEN is not set in environment")
        return

    bot = Bot(token)
    bot.delete_webhook()
    print("webhook deleted")


if __name__ == "__main__":
    main()
