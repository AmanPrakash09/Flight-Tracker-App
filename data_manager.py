import os
import requests

SHEET_ENDPOINT = "https://api.sheety.co/0f0ff9568a9353d4103bade30554404e/flightDeals/prices"

USER_ENDPOINT = "https://api.sheety.co/0f0ff9568a9353d4103bade30554404e/flightDeals/users"


class DataManager:
    def __init__(self):
        self.sheet_response = requests.get(url=SHEET_ENDPOINT)
        self.sheet_response.raise_for_status()
        self.data = self.sheet_response.json()
        self.sheet_data = self.data["prices"]
        self.firstname = ""
        self.lastname = ""
        self.email = ""

    def get_data(self):
        return self.sheet_data

    def update_data(self):
        for row in self.sheet_data:
            new_data = {
                "price": {
                    "iataCode": row["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEET_ENDPOINT}/{row['id']}",
                json=new_data
            )
            print(response.text)

    def update_price(self, new_low, id):
        new_price = {
            "price": {
                "lowestPrice": new_low
            }
        }
        response = requests.put(
            url=f"{SHEET_ENDPOINT}/{id}",
            json=new_price
        )
        print(response.text)

    def add_user(self):
        print("Welcome to Aman's Flight Club!")
        print("I am Aman's code personified! My job is to find the best flight deals for you!\n")
        self.firstname = input("What is your first name?: ").title()
        self.lastname = input("What is your last name?: ").title()
        self.email = input("What is your email?: ").lower()
        print("Welcome to the Flight Club!")
        new_user = {
            "user": {
                "firstName": self.firstname,
                "lastName": self.lastname,
                "email": self.email
            }
        }

        response = requests.post(
            url=USER_ENDPOINT,
            json=new_user
        )
        print(response.text)
