from datetime import datetime
from peewee import *
# from data.config import DB_NAME, DB_USER, DB_HOST, DB_PASSWORD, DB_PORT

# db = PostgresqlDatabase(DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
db = SqliteDatabase("mydb.db")


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    user_id = BigIntegerField(primary_key=True, unique=True)
    username = CharField(max_length=50, null=True)
    full_name = CharField(max_length=155)
    date = TimestampField()

    class Meta:
        db_name = 'users'


class Sellers(BaseModel):
    username = CharField(max_length=255, unique=True)
    status = CharField(choices=[("trusted", "Trusted"), ("scam", "Scam")])
    index = IntegerField()
    date = TimestampField()

    class Meta:
        table_name = "sellers"


class Shops(BaseModel):
    name = CharField(max_length=255)
    username = CharField(max_length=255, unique=True)
    description = TextField(null=True)
    status = CharField(choices=[("trusted", "Trusted"), ("scam", "Scam")])
    index = IntegerField()
    date = TimestampField()

    class Meta:
        table_name = "shops"