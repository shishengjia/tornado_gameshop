import peewee_async
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings = {
    "appid": "2016092100558978",
    "private_key_path": os.path.join(BASE_DIR, 'apps/utils/pay/private_2048.txt'),
    "ali_pub_key_path": os.path.join(BASE_DIR, 'apps/utils/pay/alipay_key.txt'),
    "jwt_expire": 7*24*3600,
    "secret_key": "bfV4YhRg5Z6e5eMR",
    "redis": {
        "host": "127.0.0.1"
    }
}

mysql_db = peewee_async.MySQLDatabase("GameShop2", host="127.0.0.1", port=3306, user="root", password="ssjusher123")