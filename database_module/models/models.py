from datetime import datetime
from typing import List, Optional

from peewee import *

db = SqliteDatabase('database.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField()
    user_id = IntegerField(unique=True)
    chat_id = IntegerField()


class History(BaseModel):
    command = CharField()
    user = ForeignKeyField(User, backref='Searches')
    date_time = DateTimeField()
    city = CharField()
    city_id = CharField()
    date_check_in = DateField()
    date_check_out = DateField()
    hotels_num = IntegerField()
    min_price = IntegerField(null=True)
    max_price = IntegerField(null=True)


class Hotel(BaseModel):
    hotels_search = ForeignKeyField(History, backref='hotels')
    name = CharField()
    hotel_id = IntegerField()
    address = CharField()
    price = FloatField()


def create_tables() -> None:
    with db:
        db.create_tables([User, History, Hotel])


def save_data(data: dict) -> None:
    with db.atomic():
        user = User.get_or_create(
            name=data['user_name'],
            user_id=data['user_id'],
            chat_id=data['chat_id']
        )[0]

        hotels_search = History.create(
            command=data['command'],
            user=user,
            city=data['city'],
            city_id=data['city_id'],
            date_time=datetime.strptime(data['date_time'], '%d.%m.%Y %H:%M:%S'),
            date_check_in=datetime.strptime(data['date_check_in'], '%d/%m/%Y'),
            date_check_out=datetime.strptime(data['date_check_out'], '%d/%m/%Y'),
            hotels_num=data['hotels_num'],
            min_price=data.get('min_price'),
            max_price=data.get('max_price')
        )

        for i_hotel in data['hotels']:
            hotel = Hotel.create(
                    hotels_search=hotels_search,
                    name=i_hotel['hotel'],
                    hotel_id=i_hotel['hotel_id'],
                    address=i_hotel['address'],
                    price=i_hotel['price']
            )


def hotels_history(user_id: int) -> List[History]:
    with db.atomic():
        query = History.select().join(User).where(User.user_id == user_id)
    query: list = list(query)

    return query


def hotels_history_data(search: History) -> list:
    with db.atomic():
        query = Hotel.select().where(Hotel.hotels_search == search)

    hotels = list()
    for hotel in query:
        hotels.append({
            'hotel': hotel.name,
            'hotel_id': hotel.hotel_id,
            'address': hotel.address,
            'price': hotel.price
        })

    return hotels


def days_history(hotels_search: History) -> int:
    return (hotels_search.date_out - hotels_search.date_in).days
