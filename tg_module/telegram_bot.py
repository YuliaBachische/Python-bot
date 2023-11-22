import telebot
from telebot import types
from api_module import api_handler
from database_module import database_handler
import settings

bot = telebot.TeleBot(settings.telegram_bot_token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я готов к работе. Используйте /help, чтобы узнать "
                                      "доступные команды.")


@bot.message_handler(commands=['help'])
def help(message):
    # Вывести справочную информацию
    bot.send_message(message.chat.id, "Список команд:\n/help - получить справку\n"
                                      "/low - вывод минимальных показателей\n/high - вывод "
                                      "максимальных показателей\n/custom - вывод пользовательского "
                                      "диапазона\n/history - вывод истории запросов")


@bot.message_handler(commands=['low'])
def low(message):
    # Реализация команды /low
    pass


@bot.message_handler(commands=['high'])
def high(message):
    # Реализация команды /high
    pass


@bot.message_handler(commands=['custom'])
def custom(message):
    # Реализация команды /custom
    pass


@bot.message_handler(commands=['history'])
def history(message):
    pass


@bot.message_handler(func=lambda message: True)
def unknown(message):
    bot.reply_to(message, "Извините, не понимаю эту команду. Используйте "
                          "/help, чтобы увидеть список доступных команд.")


bot.polling(none_stop=True)
