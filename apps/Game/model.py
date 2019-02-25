from tornado_gameshop.model import BaseModel
from peewee import *
from datetime import datetime
from tornado_gameshop.settings import mysql_db


class GameTag(Model):
    name = CharField(max_length=20, verbose_name="gametag")
    add_time = DateTimeField(default=datetime.now)

    class Meta:
        database = mysql_db


class Game(Model):
    name = CharField(max_length=200, verbose_name="name")
    game_detail_url = CharField(max_length=300, verbose_name="game_detail_url")
    cover_url = CharField(max_length=300, verbose_name="cover_detail_url")
    price = IntegerField(default=100, verbose_name="price")
    tag = ForeignKeyField(GameTag, verbose_name="gametype", null=True)
    os = CharField(max_length=1000, verbose_name="os")
    desc = TextField(verbose_name="description")
    release_time = DateTimeField(default=datetime.now, verbose_name="releasetime")
    game_scree_shot_1 = CharField(max_length=500, verbose_name="cover_detail_url")
    game_scree_shot_2 = CharField(max_length=500, verbose_name="cover_detail_url")
    game_scree_shot_3 = CharField(max_length=500, verbose_name="cover_detail_url")

    @classmethod
    def extend(cls):
        return cls.select(cls, GameTag.name).join(GameTag)

    class Meta:
        database = mysql_db


class Comment(Model):
    game = ForeignKeyField(Game, verbose_name="game2", null=True)
    comment = TextField(verbose_name="comment")

    @classmethod
    def extend(cls):
        return cls.select(cls, Game.id).join(Game)

    class Meta:
        database = mysql_db