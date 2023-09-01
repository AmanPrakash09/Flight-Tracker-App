from twilio.rest import Client
import smtplib
import requests

ACCOUNT_SID = "AC10d8c2309f0aaa689b4647c1d03888ed"
AUTH_TOKEN = "a748b429f9ff61e051295b18bdbf21d7"
GMAIL = "amanprakashpython@gmail.com"
APP_PASSWORD = "ulnmhrogklrcfuck"

FROM_NUMBER = "+12562545697"
TO_NUMBER = "+17787516483"

USER_ENDPOINT = "https://api.sheety.co/0f0ff9568a9353d4103bade30554404e/flightDeals/users"


class NotificationManager:
    def __init__(self):
        self.user_response = requests.get(url=USER_ENDPOINT)
        self.user_response.raise_for_status()
        self.user_data = self.user_response.json()
        self.account_sid = ACCOUNT_SID
        self.auth_token = AUTH_TOKEN
        self.gmail = GMAIL
        self.app_password = APP_PASSWORD

    def send_sms(self, body):
        client = Client(self.account_sid, self.auth_token)
        message = client.messages \
            .create(body=body, from_=FROM_NUMBER, to=TO_NUMBER)

        print(message.status)

    def send_email(self, body):
        for user in self.user_data["users"]:
            email = user["email"]
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=self.gmail, password=self.app_password)
                connection.sendmail(from_addr=self.gmail,
                                    to_addrs=email,
                                    msg=body)
            # print(self.user_data["users"])
