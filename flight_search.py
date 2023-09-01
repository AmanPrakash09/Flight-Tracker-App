import os
import requests
from datetime import datetime, timedelta
from flight_data import FlightData


time_now = datetime.now()
date_from = time_now.strftime("%d/%m/%Y")
date_to = (time_now + timedelta(days=180)).strftime("%d/%m/%Y")

API_KEY = "F1RvzRXtnJCUADHotJ32NOiqvOdLJV51"


class FlightSearch:
    def __init__(self):
        self.parameters = {}
        self.headers = {}

    def get_code(self, city_name):
        self.parameters = {
            "term": city_name,
            "location_types": "city"
        }
        self.headers = {
            "apikey": API_KEY
        }

        response = requests.get(url="https://tequila-api.kiwi.com/locations/query", params=self.parameters,
                                headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return data["locations"][0]["code"]

    def search_flights(self, city_code):
        self.parameters = {
            "fly_from": "YVR",
            "fly_to": city_code,
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }

        self.headers = {
            "apikey": API_KEY
        }
        response = requests.get(url="https://tequila-api.kiwi.com/v2/search", params=self.parameters,
                                headers=self.headers)
        response.raise_for_status()

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {city_code}.")
            return None
        else:
            cad = int(data["conversion"]["GBP"] * 1.55)
            flight_data = FlightData(
                price=cad,
                origin_city=data["cityFrom"],
                origin_airport=data["flyFrom"],
                destination_city=data["cityTo"],
                destination_airport=data["flyTo"],
                out_date=data["local_departure"].split("T")[0],
                return_date=data["local_departure"].split("T")[0],
                destination_code=city_code
            )
            print(f"{flight_data.destination_city}: {flight_data.price} CAD")
            return flight_data
