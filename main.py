import requests
import time
import winsound

mocked_data = {
    "data": {
        "trains": [
            {
                "trip_number": "SUBORNO EXPRESS (702)",
                "departure_date_time": "12 Dec, 04:30 pm",
                "departure_full_date": "2024-12-12",
                "departure_date_time_jd": "Thu, 12 Dec 2024, 04:30 PM",
                "arrival_date_time": "12 Dec, 09:25 pm",
                "travel_time": "04h 55m",
                "origin_city_name": "dhaka",
                "destination_city_name": "chattogram",
                "seat_types": [
                    {
                        "key": 3,
                        "type": "SNIGDHA",
                        "trip_id": 8373486,
                        "trip_route_id": 51386434,
                        "route_id": 22014,
                        "fare": "743.00",
                        "vat_percent": 15,
                        "vat_amount": 112,
                        "seat_counts": {"online": 1, "offline": 0, "is_divided": True},
                    },
                    {
                        "key": 7,
                        "type": "S_CHAIR",
                        "trip_id": 8373554,
                        "trip_route_id": 51388361,
                        "route_id": 22014,
                        "fare": "450.00",
                        "vat_percent": 0,
                        "vat_amount": 0,
                        "seat_counts": {"online": 3, "offline": 0, "is_divided": True},
                    },
                ],
                "train_model": "702",
                "is_open_for_all": True,
                "is_eid_trip": 0,
                "boarding_points": [
                    {
                        "trip_point_id": 107054195,
                        "location_id": 2719,
                        "location_name": "Kamalapur Station",
                        "location_time": "04:30 PM",
                    }
                ],
                "is_international": 0,
                "is_from_city_international": False,
            }
        ]
    }
}

def fetch_data():
    url = "https://railspaapi.shohoz.com/v1.0/web/bookings/search-trips-v2"
    params = {
        "from_city": "Dhaka",
        "to_city": "Chattogram",
        "date_of_journey": "12-Dec-2024",
        "seat_class": "S_CHAIR",
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None




def check_seat_availability():
    train_name="SUBORNO EXPRESS (702)"
    data = fetch_data()
    # data = mocked_data
    if not data or "data" not in data or "trains" not in data["data"]:
        print("No valid data received.")
        return

    trains = data["data"]["trains"]

    for train in trains:
        if train.get("trip_number") == train_name:
            for seat_type in train["seat_types"]:
                if seat_type.get('key')==3 or seat_type.get('key')==7:
                    seat_counts= seat_type.get('seat_counts')
                    if seat_counts.get('online')>0:
                        print(f"{seat_type.get('type')} - {seat_counts.get('online')} : seats available! Notifying...")
                        if seat_type.get('key')==3:
                             winsound.Beep(1000, 1000)
                        if seat_type.get('key') == 7:
                            winsound.Beep(1500, 500)

                    else:
                        print(f"{seat_type.get('type')} : seats are not sufficient.")



if __name__ == "__main__":
    while True:
        check_seat_availability()
        time.sleep(5)