from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_data()

new_user = input("Are you a new user? Type 'yes' or 'no': ").lower()
if new_user == "yes":
    data_manager.add_user()

for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = FlightSearch().get_code(row["city"])

data_manager.update_data()

flight_data_list = []

for row in sheet_data:
    flight_data_list.append(FlightSearch().search_flights(row["iataCode"]))

for data in flight_data_list:
    for row in sheet_data:
        if data is not None:
            if data.destination_code == row["iataCode"] and data.price < row["lowestPrice"]:
                text = f"""
                Low Price Alert! Only {data.price} CAD to fly from {data.origin_city}-{data.origin_airport}
                to {data.destination_city}-{data.destination_airport}, from {data.out_date} to {data.return_date}.\n
                Click the link below to book via Google Flights!\n
                https://www.google.co.uk/flights?hl=en#flt={data.origin_airport}.{data.destination_code}.{data.out_date}*{data.destination_code}.{data.origin_airport}.{data.return_date}
                """
                NotificationManager().send_sms(text)
                NotificationManager().send_email(text)
                data_manager.update_price(data.price, row["id"])

try:
    print(flight_data_list[0].destination_code)
except:
    print("None")
