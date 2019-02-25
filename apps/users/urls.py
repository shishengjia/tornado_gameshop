from tornado.web import url
from apps.users.handler import SmsHandler, RegisterHandler, OrderHandler, UserStarGameHandler, \
    UserInfoHandler, UserOrderHandler, CollectGameHandler, LoginHandler

url_pattern = (
    url("/v1/code/", SmsHandler),
    url("/v1/register/", RegisterHandler),
    url("/v1/login/", LoginHandler),
    url("/v1/order/", OrderHandler),
    url("/v1/user_orders/", UserOrderHandler),
    url("/v1/user_game/", UserStarGameHandler),
    url("/v1/user_info/", UserInfoHandler),
    url("/v1/game/star/", CollectGameHandler)
)
