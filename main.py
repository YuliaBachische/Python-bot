from telebot.custom_filters import StateFilter
from load_bot import bot
from database_module.models.models import create_tables
from loguru import logger


def configure_logger():
    logger.add("app.log", rotation="500 MB", level="DEBUG")


if __name__ == '__main__':
    configure_logger()
    logger.debug('Бот запущен')

    create_tables()

    bot.add_custom_filter(StateFilter(bot))

    bot.infinity_polling()