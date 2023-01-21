import json
import math
import random
import typing as t
from datetime import datetime, timedelta
from logging import getLogger

import more_itertools
from joblib import Parallel, delayed
from pymongo import MongoClient


log = getLogger(__name__)


mongodb = MongoClient("mongodb://router-01:27017")
LOCATIONS = list(mongodb.london.postcodes.find({}, ["_id", "lat", "long"]))


def calculate_distance(
    start: tuple[float, float],
    end: tuple[float, float],
) -> float:
    lat1, lon1 = start
    lat2, lon2 = end

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(
        math.radians(lat1)
    ) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    distance = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)) * 6371

    return distance


def calculate_price(doc: dict[str, t.Any]) -> float:
    start_loc = doc["start_location"]
    end_loc = doc["end_location"]

    origin = start_loc["lat"], start_loc["long"]
    destination = end_loc["lat"], end_loc["long"]

    return calculate_distance(origin, destination) * 5.5


def create_driver_review() -> dict[str, t.Any]:
    categories = [
        "fast",
        "confortable",
        "polite",
    ]

    reviews = [
        'aaaa',
        'bbbbb',
        'cccccc',
        'dddddd',
    ]

    driver_review = {}
    if random.random() < 0.7:

        driver_review["rating"] = random.randrange(5)

        if random.random() < 0.3:
            num_cat = random.randint(1, len(categories))
            driver_review["categories"] = random.sample(
                categories,
                num_cat,
            )

        if random.random() < 0.2:
            driver_review["text"] = random.choice(reviews)

    return driver_review


def create_client_review() -> dict[str, t.Any]:
    categories = [
        "super",
        "communicative",
    ]
    client_review = {}

    if random.random() < 0.7:
        client_review["rating"] = random.randrange(5)
        if random.random() < 0.3:
            num_cat = random.randint(1, len(categories))
            client_review["categories"] = random.sample(
                categories,
                num_cat,
            )
    return client_review


def create_record() -> dict[str, t.Any]:
    day = timedelta(days=random.randrange(31))
    duration = timedelta(minutes=random.randint(10, 160))

    doc = {
        "driver_id": random.randrange(1000),
        "client_id": random.randrange(1000),
        "start_date":  datetime.now() + day,
        "end_date":  datetime.now() + day + duration,
        "start_location": random.choice(LOCATIONS),
        "end_location": random.choice(LOCATIONS),
    }

    doc["cost"] = calculate_price(doc)

    if driver_review := create_driver_review():
        doc["driver_review"] = driver_review

    if client_review := create_client_review():
        doc["client_review"] = client_review

    log.info(f'Doc generated: {doc}')
    return doc


if __name__ == "__main__":
    chunks = more_itertools.chunked(
        (create_record() for _ in range(10000)),
        10,
    )

    log.info(f'Chucks generated')

    mongodb.admin.command(
        {"shardCollection": "london.taxi_rides",
         "key": {"_id": "hashed"}},
    )
    task = Parallel(4, backend="threading")
    task(delayed(mongodb.london.taxi_rides.insert_many)(x) for x in chunks)

    log.info('Generation finished')
