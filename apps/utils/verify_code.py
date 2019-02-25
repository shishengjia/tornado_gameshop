import requests

# api_key = "1ef13fed55f8f78d2768b96c6879deb4"


class Verify_code:
    def __init__(self):
        self.api_key = "1ef13fed55f8f78d2768b96c6879deb4"

    def send_single_sms(self, code, phone_number):
        url = "https://sms.yunpian.com/v2/sms/single_send.json"
        text = "【施圣佳测试】您的验证码是{}。如非本人操作，请忽略本短信".format(code)

        res = requests.post(url, data={
            "apikey": self.api_key,
            "mobile": phone_number,
            "text": text
        })

        return res.text


c = Verify_code()
print(c.send_single_sms(12345, "18575530799"))