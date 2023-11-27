from keyboa import Keyboa
from telebot.types import InlineKeyboardMarkup

hotels_markup = Keyboa(items=list(range(1, 11)),
                       items_in_row=6)


def hotels_search_markup(hotels_id: int) -> InlineKeyboardMarkup:

    return Keyboa(
        items={
            "text": 'Показать результаты поиска',
            "callback_data": str(hotels_id),
        }
    ).keyboard