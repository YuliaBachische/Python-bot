import os
from dotenv import load_dotenv

# Загрузка переменных из файла .env
load_dotenv()

# Получение значений переменных
telegram_bot_token = os.getenv("BOT_TOKEN")
site_api = os.getenv("SITE_API")


