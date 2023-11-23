from telebot import TeleBot
from telebot.storage import StateMemoryStorage
import settings

storage = StateMemoryStorage()
bot = TeleBot(token=settings.telegram_bot_token, state_storage=storage)