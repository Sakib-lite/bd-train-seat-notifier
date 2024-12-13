import datetime
import logging
import time

import requests
import winsound

from config import FROM, TO, JOURNEY_DATE, CURRENT_TRAIN, SEATS

log_file = "seat_availability.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),

    ]
)


def fetch_data():
    try:
        url = "https://railspaapi.shohoz.com/v1.0/web/bookings/search-trips-v2"
        params = {
            "from_city": FROM,
            "to_city": TO,
            "date_of_journey": JOURNEY_DATE,
            "seat_class": "S_CHAIR",
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Error fetching data: {response.status_code}")
            return None
    except Exception as e:
        logging.exception("Exception occurred while fetching data:")
        winsound.Beep(800, 1000)
        return None


def check_seat_availability(): 
    try:

        data = fetch_data()
        # data =  mocked_data

        if not data or "data" not in data or "trains" not in data["data"]:
            logging.warning("No valid data received.")
            return

        trains = data["data"]["trains"]

        for train in trains:
            if train.get("trip_number") == CURRENT_TRAIN:
                for seat_type in train["seat_types"]:
                    if seat_type.get('key') in list(SEATS.values()):
                        seat_counts = seat_type.get('seat_counts')
                        if seat_counts.get('online') > 0:
                            log_message = f"{seat_type.get('type')} - {seat_counts.get('online')} seats available! Notifying..."
                            print(log_message)
                            logging.info(log_message)
                            if seat_type.get('key') == SEATS['SUVON_CHAIR']:
                                winsound.Beep(1000, 1000)
                            # elif seat_type.get('key') == SUVON_CHAIR_KEY:
                            #     winsound.Beep(1500, 1000)
                        else:
                            logging.info(
                                f"{seat_type.get('type')} - Seats are not sufficient. {datetime.datetime.now()} - {seat_type.get('seat_counts')}")
    except Exception as e:
        logging.exception("Exception occurred while checking seat availability:")
        winsound.Beep(500, 1000)


if __name__ == "__main__":
    while True:
        check_seat_availability()
        time.sleep(3)
