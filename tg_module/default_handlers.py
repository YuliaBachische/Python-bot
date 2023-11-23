from load_bot import bot
from telebot.types import Message
from loguru import logger


@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
    """
    Начало работы с ботом
    :param message: команда от пользователя
    :return: None
    """
    logger.info(f' Отправлена команда: {message.text})')

    bot.send_message(message.chat.id, "Привет! Я готов к работе. Используйте /help, чтобы узнать "
                                      "доступные команды.")


@bot.message_handler(commands=['help'])
def bot_help(message: Message) -> None:
    logger.info(f' Отправлена команда: {message.text})')

    # Вывести справочную информацию
    bot.send_message(message.chat.id, "Список команд:\n/help - получить справку\n"
                                      "/low - вывод минимальных показателей\n/high - вывод "
                                      "максимальных показателей\n/custom - вывод пользовательского "
                                      "диапазона\n/history - вывод истории запросов")
