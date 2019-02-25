import functools
import jwt

from apps.users.model import User


def authenticated_async(method):
    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):
        re_data = {"success": False, "data": "Authentication Failed"}
        # 请求是否有jwt生成的 token
        token = self.request.headers.get("token", None)
        if token:
            try:
                # 从token里 解密出 用户id
                send_data = jwt.decode(token, self.settings["secret_key"], leeway=self.settings["jwt_expire"],
                                       options={"verify_exp": True})
                user_id = send_data["id"]

                # 从数据库中获取到user并设置给_current_user
                try:
                    user = await self.application.objects.get(User, id=user_id)
                    self._current_user = user

                    await method(self, *args, **kwargs)
                except User.DoesNotExist as e:
                    self.set_status(401)
                    self.finish(re_data)
            except jwt.ExpiredSignatureError as e:
                self.set_status(401)
                self.finish(re_data)
        else:
            self.set_status(401)
            self.finish(re_data)
    return wrapper
