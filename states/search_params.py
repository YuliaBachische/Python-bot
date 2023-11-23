from telebot.handler_backends import State, StatesGroup


class SearchParamsState(StatesGroup):

    city = State()
    get_city = State()
    date_check_in = State()
    date_check_out = State()
    min_price = State()
    max_price = State()
    photos = State()
    hotels_num = State()
    result = State()
