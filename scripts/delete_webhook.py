import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"

r = requests.get(url)
print(r.text)