import requests
from tornado_gameshop.handler import RedisHandler, BaseHandler
from apps.utils.verify_code_async import AsyncVerifyCode
from apps.users.forms import SmsCodeForm, RegisterForm, LoginFrom
from apps.users.model import User
from apps.utils.my_decorator import authenticated_async
from apps.utils.pay.alipay import AliPay
from apps.operation.model import Order, UserGame, UserFavorite
from peewee import JOIN
from apps.Game.model import Game
from peewee_async import Manager
from tornado_gameshop.settings import mysql_db
import asyncio


web_url = "http://127.0.0.1:8888"


def test_send_sms(mobile):
    url = "{}/code/".format(web_url)

    data = {
        "mobile": mobile
    }

    res = requests.post(url, json=data)

    print(res.text)


def test_register(mobile):
    url = "{}/register/".format(web_url)

    data = {
        "mobile": mobile,
        "code": "7907",
        "password": "ssjusher123"
    }

    res = requests.post(url, json=data)

    print(res.text)


def test_login(mobile):
    url = "{}/login/".format(web_url)

    data = {
        "mobile": mobile,
        "password": "ssjusher123"
    }

    res = requests.post(url, json=data)

    print(res.text)


def test_order():
    url = "{}/order/".format(web_url)

    data = {
        "game_id": 2,
        "subject": "PS4",
        "total_amount": 100,
        "out_trade_no": "201312313212323",
        "notify_url": "https://www.baidu.com",
        "return_url": "https://www.baidu.com"
    }
    headers = {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwibmlja19uYW1lIjpudWxsLCJleHAiOjE1NTEwMTU5ODN9.mLcAoD9u-MmnezBinnWDUcWYe9fEPiA4A-KJK_1rg14"
    }

    res = requests.post(url, json=data, headers=headers)

    print(res.text)


def test_collect():
    url = "{}/game/star/".format(web_url)

    data = {
        "game_id": 22,
    }
    headers = {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwibmlja19uYW1lIjpudWxsLCJleHAiOjE1NTEwMTU5ODN9.mLcAoD9u-MmnezBinnWDUcWYe9fEPiA4A-KJK_1rg14"
    }

    res = requests.post(url, json=data, headers=headers)

    print(res.text)

def test_user_info():
    url = "{}/user_info/".format(web_url)

    headers = {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwibmlja19uYW1lIjpudWxsLCJleHAiOjE1NTEwMTU5ODN9.mLcAoD9u-MmnezBinnWDUcWYe9fEPiA4A-KJK_1rg14"
    }

    res = requests.get(url, headers=headers)

    print(res.text)

def test_user_star_game():
    url = "{}/user_game/".format(web_url)

    headers = {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwibmlja19uYW1lIjpudWxsLCJleHAiOjE1NTEwMTU5ODN9.mLcAoD9u-MmnezBinnWDUcWYe9fEPiA4A-KJK_1rg14"
    }

    res = requests.get(url, headers=headers)

    print(res.text)

async def query():
    query = UserFavorite.select().where(UserFavorite.user_id == 1)

    game_ids = await Manager(mysql_db).execute(query)
    ids = []
    for id in game_ids:
        ids.append(id.id)

    games = await Manager(mysql_db).execute(Game.select().where(Game.id.in_(ids)))

    for game in games:
        print(game.name)

if __name__ == "__main__":
    test_user_star_game()

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(query())

