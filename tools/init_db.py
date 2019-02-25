from apps.users.model import User
from apps.Game.model import Game, GameTag, Comment
from apps.operation.model import UserGame, UserFavorite, Order

from tornado_gameshop.settings import mysql_db



def init():
    mysql_db.create_tables([UserFavorite, UserGame, Order])


if __name__ == "__main__":
    init()