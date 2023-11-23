from typing import List

from database_module.models.models import History
from keyboards.inline.hotels import hotels_search_markup
from load_bot import bot


def format_hotel_text(hotels: List[dict], user_id: int, days: int) -> None:
    formatted_text = ""

    for num, hotel in enumerate(hotels, start=1):
        hotel_name = hotel.get("hotel", "")
        address = hotel.get("address", "нет данных")
        price_per_day = hotel.get("price", 0)

        text = (
            f'Отель {num}:\n'
            f'Название: <b>{hotel_name}</b>\n'
            f'Адрес: <b>{address}</b>\n'
            f'Цена за один день: <b>{price_per_day:.1f} $.</b>\n'
            f'Цена за все дни (дней - {days}): '
            f'<b>{price_per_day * days:.1f} $.</b>\n\n'
        )

        formatted_text += text

        bot.send_message(user_id, text, parse_mode='HTML')


def hotels_searches_output(hotels_searches: List[History],
                           user_id: int) -> None:

    for index, search in enumerate(hotels_searches):
        command_text = f'<b>Команда:</b> {search.command}'
        datetime_text = f'<b>Дата и время поиска:</b> {search.date_time.strftime("%d.%m.%Y %H:%M:%S")}'
        city_text = f'<b>Место для поиска:</b> {search.city}'
        check_in_text = f'<b>Дата заселения:</b> {search.date_check_in.strftime("%d.%m.%Y")}'
        check_out_text = f'<b>Дата выселения:</b> {search.date_check_out.strftime("%d.%m.%Y")}'
        hotels_num_text = f'<b>Количество отелей:</b> {search.hotels_num}'

        price_texts = []
        if search.min_price:
            price_texts.append(f'<b>Минимальная цена за сутки:</b> {search.min_price}')
        if search.max_price:
            price_texts.append(f'<b>Максимальная цена за сутки:</b> {search.max_price}')
        prices_text = '\n'.join(price_texts)

        message_text = '\n'.join([command_text, datetime_text, city_text,
                                  check_in_text, check_out_text, hotels_num_text, prices_text])

        bot.send_message(user_id, message_text, parse_mode='HTML',
                         reply_markup=hotels_search_markup(search.get_id()))