from tornado import web, ioloop
import tornado
import wtforms_json
from peewee_async import Manager
from tornado_gameshop.settings import mysql_db

from tornado_gameshop.urls import url_pattern
from tornado_gameshop.settings import settings


if __name__ == "__main__":
    wtforms_json.init()
    app = web.Application(url_pattern, debug=True, **settings)
    app.listen(8888)

    objects = Manager(mysql_db)
    mysql_db.set_allow_sync(False)

    app.objects = objects

    ioloop.IOLoop.current().start()

