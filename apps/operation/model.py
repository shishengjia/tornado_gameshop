# -*- encoding: utf-8 -*-
from peewee import *
from datetime import datetime
from tornado_gameshop.settings import mysql_db
from apps.users.model import User
from apps.Game.model import Game


class UserFavorite(Model):
    user = ForeignKeyField(User, verbose_name="user")
    fav_game_id = IntegerField(default=0, verbose_name="fav_game_id")
    add_time = DateTimeField(default=datetime.now, verbose_name="addtime")

    class Meta:
        database = mysql_db


class UserGame(Model):
    user = ForeignKeyField(User, verbose_name="user")
    game = ForeignKeyField(Game, verbose_name="game")
    add_time = DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        database = mysql_db



class Order(Model):

    user = ForeignKeyField(User, verbose_name="user")
    game = ForeignKeyField(Game, verbose_name="game")
    out_trade_no = CharField(max_length=100, unique=True, null=True, verbose_name="merchant trade_no")
    trade_no = CharField(max_length=100, unique=True, null=True, verbose_name="pay trade_no")
    pay_status = CharField(default="wait_for_pay", max_length=30, verbose_name="pay_status")
    order_amount = FloatField(default=0.0, verbose_name="order_amount")
    pay_time = DateTimeField(null=True, verbose_name="pay_time")
    add_time = DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        database = mysql_db

