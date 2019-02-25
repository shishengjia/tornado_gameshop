from tornado.web import RequestHandler
from random import choice
import json
import jwt
from datetime import datetime
import logging

from tornado_gameshop.handler import RedisHandler, BaseHandler
from apps.utils.verify_code_async import AsyncVerifyCode
from apps.users.forms import SmsCodeForm, RegisterForm, LoginFrom
from apps.users.model import User
from apps.utils.my_decorator import authenticated_async
from apps.utils.pay.alipay import AliPay
from apps.operation.model import Order, UserGame, UserFavorite
from apps.Game.model import Game


def generate_code(length=4):
    seeds = "1234567890"
    random_str = []

    for i in range(length):
        random_str.append(choice(seeds))

    return "".join(random_str)


class SmsHandler(RedisHandler):
    """
    发送短信验证码
    """
    async def post(self, *args, **kwargs):
        re_data = {}

        param = self.request.body.decode("utf8")
        param = json.loads(param)

        # django tornado框架会把传来的值包装成list，form会迭代出第一个值， 如果自己直接传来字符串，只会迭代出第一个字符
        # wtforms_json 对 form 进行了包装，动态加入了 from_json 方法 来解决这个问题
        sms_form = SmsCodeForm.from_json(param)
        if sms_form.validate():

            verify_code = generate_code()
            mobile = sms_form.mobile.data

            code = AsyncVerifyCode(verify_code, mobile)

            # 发送短信验证码
            re_json = await code.send_single_sms()

            if re_json["code"] != 0:
                self.set_status(400)
                re_data["mobile"] = re_json["msg"]
            else:
                # 写入redis并设置过期时间为10分钟
                self.redis_conn.set("{}_{}".format(mobile, verify_code), 1, 10*60)

        else:
            self.set_status(400)
            for field in sms_form.errors:
                re_data[field] = sms_form.errors[field][0]

        self.finish(re_data)


class RegisterHandler(RedisHandler):
    """
    用户注册
    """
    async def post(self, *args, **kwargs):
        re_data = {}

        param = self.request.body.decode("utf8")
        param = json.loads(param)
        register_form = RegisterForm.from_json(param)
        if register_form.validate():
            mobile = register_form.mobile.data
            code = register_form.code.data
            password = register_form.password.data

            # 验证码是否正确
            redis_key = "{}_{}".format(mobile, code)

            # 也可以用异步的redis库，但是redis本身是内存操作，性能上能够满足
            if not self.redis_conn.get(redis_key):
                self.set_status(400)
                re_data["code"] = "验证码失效或者错误"
            else:
                # 验证用户是否已经存在
                try:
                    exists_user = await self.application.objects.get(User, mobile=mobile)
                    self.set_status(400)
                    re_data["mobile"] = "用户已存在"
                except User.DoesNotExist as e:
                    # 用户不存在
                    user = await self.application.objects.create(User, mobile=mobile, password=password)
                    re_data["id"] = user.id

        else:
            self.set_status(400)
            for field in register_form.errors:
                re_data[field] = register_form[field]

        self.finish(re_data)


class LoginHandler(RedisHandler):
    """
    用户登录
    """
    async def post(self, *args, **kwargs):
        re_data = {}

        param = self.request.body.decode("utf-8")
        param = json.loads(param)

        form = LoginFrom.from_json(param)

        if form.validate():
            mobile = form.mobile.data
            password = form.password.data

            try:
                user = await self.application.objects.get(User, mobile=mobile)
                if not user.password.check_password(password):
                    self.set_status(400)
                    re_data["non_fields"] = "用户名或密码错误"
                else:
                    #登录成功
                    payload = {
                        "id": user.id,
                        "mobile": user.mobile,
                        "exp": datetime.utcnow()
                    }
                    # 返回一个由用户 ID和mobile 生成的 加密token给客户端，客户端每次发过来做验证用
                    token = jwt.encode(payload, self.settings["secret_key"], algorithm='HS256')
                    re_data["id"] = user.id
                    re_data["token"] = token.decode("utf8")

            except User.DoesNotExist as e:
                self.set_status(400)
                re_data["mobile"] = "用户不存在"

            self.finish(re_data)


class OrderHandler(BaseHandler):
    """
    根据用户传来的商品信息，生成支付宝付款链接并返回
    """
    @authenticated_async
    async def post(self, *args, **kwargs):
        re_data = {}
        try:
            param = self.request.body.decode("utf-8")
            param = json.loads(param)

            game_id = param["game_id"]
            notify_url = param["notify_url"]
            return_url = param["return_url"]
            subject = param["subject"]
            out_trade_no = param["out_trade_no"]
            total_amount = param["total_amount"]

            pay = AliPay(
                appid=self.settings["appid"],
                app_notify_url=notify_url,
                app_private_key_path=self.settings["private_key_path"],
                alipay_public_key_path=self.settings["ali_pub_key_path"],  # 支付宝的公钥，验证支付宝回传消息使用
                debug=True,  # 默认False,
                return_url=return_url
            )

            url = pay.direct_pay(
                subject=subject,
                out_trade_no=out_trade_no,
                total_amount=int(total_amount),
                return_url=return_url
            )

            order = await self.application.objects.create(Order, user_id=self._current_user.id, game_id=int(game_id),
                                                  out_trade_no=out_trade_no, trade_no=None,
                                                  order_amount=int(total_amount), add_time=datetime.now())

            self.set_status(200)
            re_data["success"] = True
            re_data["url"] = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        except Exception as e:
            re_data["success"] = False
            re_data["data"] = "缺少关键参数"
            self.set_status(400)

        self.finish(re_data)


class UserStarGameHandler(BaseHandler):
    """
    用户收藏的游戏
    """
    @authenticated_async
    async def get(self, *args, **kwargs):
        re_data = {"games": [], }
        try:
            query = UserFavorite.select().where(UserFavorite.user_id == 1)

            user_fav = await self.application.objects.execute(query)

            games = await self.application.objects.execute(Game.select().where(Game.id.in_([fav.id for fav in user_fav])))

            [re_data["games"].append({
                "game_id": game.id,
                "name": game.name,
                "price": game.price,
                "cover_url": game.cover_url
            }) for game in games]

            re_data["success"] = True
            self.set_status(200)
        except:
            re_data["success"] = False
            self.set_status(400)
        self.finish(re_data)


class UserInfoHandler(BaseHandler):
    """
    用户信息
    """
    @authenticated_async
    async def get(self, *args, **kwargs):
        re_data = {}
        try:
            re_data["mobile"] = self._current_user.mobile
            re_data["nick_name"] = self._current_user.nick_name
            re_data["success"] = True
            self.set_status(200)
        except:
            re_data["success"] = False
            self.set_status(400)
        self.finish(re_data)


class CollectGameHandler(BaseHandler):
    """
    取消&收藏 游戏
    """
    @authenticated_async
    async def post(self, *args, **kwargs):
        re_data = {}
        try:
            param = self.request.body.decode("utf-8")
            param = json.loads(param)

            game_id = param["game_id"]

            # 已经收藏, 则取消收藏
            try:
                record = await self.application.objects.get(UserFavorite, user_id=self._current_user.id,
                                                                   fav_game_id=game_id)
                await self.application.objects.delete(record)
                re_data["success"] = True
                re_data["data"] = "取消收藏成功"
            except UserFavorite.DoesNotExist as e:
                # 未收藏， 则收藏
                await self.application.objects.create(UserFavorite, user_id=self._current_user.id,
                                                                   fav_game_id=game_id)
                re_data["success"] = True
                re_data["data"] = "收藏成功"
            except Exception as e:
                logging.warning(e)
        except Exception as e:
            re_data["success"] = False
            re_data["data"] = "参数错误"

        self.finish(re_data)












