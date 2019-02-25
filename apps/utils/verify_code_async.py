from tornado import httpclient, ioloop
from tornado.httpclient import HTTPRequest
from functools import partial
from urllib.parse import urlencode
import json


class AsyncVerifyCode:
    def __init__(self, code, mobile):
        self.api_key = "1ef13fed55f8f78d2768b96c6879deb4"
        self.code = code
        self.mobile = mobile

    async def send_single_sms(self):
        client = httpclient.AsyncHTTPClient()
        url = "http://sms.yunpian.com/v2/sms/single_send.json"
        text = "【施圣佳测试】您的验证码是{}。如非本人操作，请忽略本短信".format(self.code)

        post_request = HTTPRequest(url=url, method="POST", body=urlencode({
            "apikey": self.api_key,
            "mobile": self.mobile,
            "text": text
        }))

        res = await client.fetch(post_request)

        return json.loads(res.body.decode("utf8"))


if __name__ == "__main__":
    loop = ioloop.IOLoop.current()

    code = AsyncVerifyCode(1234, "18575530799")


    loop.run_sync(code.send_single_sms)

