from typing import Dict
from telebot.types import InlineKeyboardMarkup
from keyboa import Keyboa


def city_markup(cities: Dict[str, str]) -> InlineKeyboardMarkup:
    cities_items = [(city, city_id) for city_id, city in cities.items()]
    return Keyboa(items=cities_items).keyboard
