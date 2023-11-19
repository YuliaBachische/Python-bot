from peewee import Model, SqliteDatabase, IntegerField, CharField, DateTimeField

db = SqliteDatabase('database.db')


class BaseModel(Model):
    class Meta:
        database = db


class History(BaseModel):
    user_id = IntegerField()
    command = CharField()
    timestamp = DateTimeField()