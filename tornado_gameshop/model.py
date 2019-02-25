from peewee import *
from datetime import datetime
from tornado_gameshop.settings import mysql_db


class BaseModel(Model):
    add_time = DateTimeField(default=datetime.now)

    class Meta:
        database = mysql_db
