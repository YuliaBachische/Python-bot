from typing import Optional, List
from api_module.api_params.city_location import city_location
from api_module.api_params.hotel_params import low_price, high_price, custom
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import date, timedelta, datetime
from telebot.types import Message, CallbackQuery
from loguru import logger
from api_module.api_params.hotel_address import hotel_address
from api_module.api_params.message_format import format_hotel_text, hotels_searches_output
from database_module.models.models import hotels_history, save_data
from keyboards.inline.hotels import hotels_markup
from states.history import history
from states.search_params import SearchParamsState
from keyboards.inline.cities import city_markup
from load_bot import bot


@bot.message_handler(commands=['low', 'high', 'custom'])
def handle_low_high_custom_command(message: Message) -> None:
    user_id = message.from_user.id
    chat_id = message.chat.id

    logger.info(f'Отправлена команда: {message.text})')
    bot.set_state(user_id, SearchParamsState.city, chat_id)
    bot.send_message(user_id, 'В каком городе вы находитесь?')

    with bot.retrieve_data(user_id, chat_id) as data:
        data['command'] = message.text
        data['date_time'] = datetime.utcnow().strftime('%d.%m.%Y %H:%M:%S')
        data['user_id'] = user_id
        data['chat_id'] = chat_id
        data['user_name'] = message.from_user.full_name


@bot.message_handler(state=SearchParamsState.city)
def handle_input_city(message: Message) -> None:
    cities_dict = city_location(message.text)
    user_id = message.from_user.id
    chat_id = message.chat.id

    logger.info(f'Отправлена команда: {message.text})')

    if cities_dict:
        with bot.retrieve_data(user_id, chat_id) as data:
            data['cities'] = cities_dict
        text = 'Укажите подробнее:'
        cities_keyboard = city_markup(cities_dict)
        bot.send_message(message.chat.id, text, reply_markup=cities_keyboard)
        bot.set_state(user_id, SearchParamsState.get_city, chat_id)
    else:
        text = 'Что-то пошло не так'
        bot.send_message(user_id, text)


@bot.callback_query_handler(func=None, state=SearchParamsState.get_city)
def location(call: CallbackQuery) -> None:

    user_id: int = call.from_user.id
    chat_id: int = call.message.chat.id
    message_id: int = call.message.message_id

    with bot.retrieve_data(user_id, chat_id) as data:
        city_id: str = call.data
        data['city_id'] = city_id
        data['city'] = data['cities'][city_id]
        del data['cities']
        the_city: str = data['city']
    text: str = f'Поиск в : {the_city}'
    bot.edit_message_text(text, chat_id, message_id)
    logger.info(text)

    calendar, step = DetailedTelegramCalendar(calendar_id=1, locale='ru',
                                              min_date=date.today()
                                              ).build()

    bot.send_message(user_id, f'Выберите дату заселения:  {LSTEP[step]}',
                     reply_markup=calendar)
    bot.set_state(user_id, SearchParamsState.date_check_in, chat_id)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1),
                            state=SearchParamsState.date_check_in)
def get_date_in(call: CallbackQuery) -> None:
    handle_date_selection(call, SearchParamsState.date_check_out, 2)


def handle_date_selection(call: CallbackQuery, next_state, next_calendar_id) -> None:
    user_id: int = call.from_user.id
    chat_id: int = call.message.chat.id
    message_id: int = call.message.message_id

    result, key, step = DetailedTelegramCalendar(calendar_id=1,
                                                 locale='ru',
                                                 min_date=date.today()
                                                 ).process(call.data)
    if not result and key:
        bot.edit_message_text(f"Выберите дату заселения {LSTEP[step]}",
                              chat_id, message_id, reply_markup=key)
    elif result:
        text: str = f"Дата заселения: {result.strftime('%d/%m/%Y')}"
        bot.edit_message_text(text, chat_id, message_id)
        logger.info(text)
        with bot.retrieve_data(user_id, chat_id) as data:
            data['date_check_in'] = result.strftime('%d/%m/%Y')
            min_date: date = result + timedelta(days=1)

        calendar, step = DetailedTelegramCalendar(calendar_id=next_calendar_id, locale='ru',
                                                  min_date=min_date
                                                  ).build()
        bot.set_state(user_id, next_state, chat_id)
        bot.send_message(user_id, f'Выберите дату выселения: {LSTEP[step]}',
                         reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2),
                            state=SearchParamsState.date_check_out)
def get_date_out(call: CallbackQuery) -> None:
    user_id: int = call.from_user.id
    chat_id: int = call.message.chat.id
    message_id: int = call.message.message_id

    with bot.retrieve_data(user_id, chat_id) as data:
        min_date: date = (datetime.strptime(data['date_check_in'], '%d/%m/%Y') +
                          timedelta(days=1)).date()
    result, key, step = DetailedTelegramCalendar(calendar_id=2,
                                                 locale='ru',
                                                 min_date=min_date
                                                 ).process(call.data)
    if not result and key:
        bot.edit_message_text(f"Выберите дату отъезда: {LSTEP[step]}",
                              chat_id, message_id, reply_markup=key)
    elif result:
        text: str = f"Дата отъезда: {result.strftime('%d/%m/%Y')}"
        bot.edit_message_text(text, chat_id, message_id)
        logger.info(text)

        with bot.retrieve_data(user_id, chat_id) as data:
            data['date_check_out'] = result.strftime('%d/%m/%Y')
        bot.set_state(user_id, SearchParamsState.hotels_num, chat_id)
        bot.send_message(user_id, 'Сколько отелей вам найти?',
                         reply_markup=hotels_markup())


@bot.callback_query_handler(func=None, state=SearchParamsState.hotels_num)
def get_hotels_num(call: CallbackQuery) -> None:
    user_id: int = call.from_user.id
    chat_id: int = call.message.chat.id
    message_id: int = call.message.message_id

    text: str = f'Количество отелей: {call.data}'
    bot.edit_message_text(text, chat_id, message_id)
    logger.info(text)
    bot.set_state(user_id, SearchParamsState.min_price, chat_id)
    with bot.retrieve_data(user_id, chat_id) as data:
        data['hotels_num'] = int(call.data)
        command: str = data['command']
        info: dict = data

    hotels = None
    waiting_text: str = 'Идет поиск...'
    if command == '/low':
        bot.send_message(user_id, waiting_text)
        hotels: Optional[List[dict]] = low_price(info)
        hotels: Optional[List[dict]] = hotel_address(hotels)

    elif command == '/high':
        bot.send_message(user_id, waiting_text)
        hotels: Optional[List[dict]] = high_price(info)
        hotels: Optional[List[dict]] = hotel_address(hotels)

    if command == '/custom':
        bot.set_state(user_id, SearchParamsState.min_price, chat_id)
        bot.send_message(user_id, 'Укажите минимальную цену за сутки ($)')
    elif hotels:
        bot.set_state(user_id, SearchParamsState.result, chat_id)
        date_check_in = datetime.strptime(info['date_check_in'], '%d/%m/%Y')
        date_check_out = datetime.strptime(info['date_check_out'], '%d/%m/%Y')
        days = (date_check_out - date_check_in).days
        format_hotel_text(hotels, info['user_id'], days)
        info['hotels'] = hotels
        save_data(info)
    else:
        text = 'Произошла ошибка. Попробуйте выполнить поиск с другими параметрами'
        bot.send_message(user_id, text)


@bot.message_handler(state=SearchParamsState.min_price)
def get_min_price(message: Message) -> None:

    user_id: int = message.from_user.id
    chat_id: int = message.chat.id

    if not message.text.isdigit():
        text: str = 'Нужно указать целое число.'
        bot.send_message(user_id, text)
    else:
        logger.info(f'Минимальная цена за день: {message.text}')
        bot.set_state(user_id, SearchParamsState.max_price, chat_id)
        bot.send_message(user_id,
                         'Укажите максимальную цену за день ($)')
        with bot.retrieve_data(user_id, chat_id) as data:
            data['min_price'] = int(message.text)


@bot.message_handler(state=SearchParamsState.max_price)
def get_max_price(message: Message) -> None:

    user_id: int = message.from_user.id
    chat_id: int = message.chat.id
    with bot.retrieve_data(user_id, chat_id) as data:
        min_price = data['min_price']

    logger.info(f'Максимальная цена за сутки: {message.text}')
    with bot.retrieve_data(user_id, chat_id) as data:
        data['max_price'] = int(message.text)
        current_info: dict = data
    hotels: Optional[List[dict]] = custom(current_info)
    if hotels:
        bot.set_state(user_id, SearchParamsState.result, chat_id)
        date_in = datetime.strptime(current_info['date_check_in'], '%d/%m/%Y')
        date_out = datetime.strptime(current_info['date_check_out'], '%d/%m/%Y')
        days = (date_out - date_in).days
        hotel_address(hotels)
        format_hotel_text(hotels, current_info['user_id'], days)
        current_info['hotels'] = hotels
    else:
        text = 'Проиошла ошибка. Попробуйте еще раз'
        bot.send_message(user_id, text)


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:

    logger.info(f'Команда: {message.text}')
    user_id: int = message.from_user.id
    chat_id: int = message.chat.id
    logger.info(f'user_id = {user_id}; chat_id = {chat_id}')

    hotels_searches = hotels_history(user_id)

    bot.send_message(user_id, f'История поисков отелей: '
                              f'{len(hotels_searches)}')
    bot.set_state(user_id, history, chat_id)
    hotels_searches_output(hotels_searches, user_id)

