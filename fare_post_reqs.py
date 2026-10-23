"""Send normal or drift-focused fare requests to the configured Taxi API."""

import argparse
import os
import random
import time
from datetime import datetime, timedelta

import requests

DEFAULT_BASE_URL = (
    "http://taxi-w5-student-alb-692350579.ap-south-2.elb.amazonaws.com"
)


def make_payload(rng: random.Random, mode: str) -> dict:
    start = datetime(2024, 3, 1)
    end = datetime(2024, 4, 1)
    pickup_time = start + timedelta(seconds=rng.randrange(int((end - start).total_seconds())))
    pickup_time = pickup_time.replace(minute=0, second=0, microsecond=0)

    if mode == "drift":
        # Shift multiple monitored numeric inputs while staying within the API
        # schema's valid ranges.
        distance = round(rng.uniform(80, 100), 2)
        passenger_count = 8
        duration = round(rng.uniform(180, 240), 2)
    else:
        distance = round(rng.uniform(1, 100), 2)
        passenger_count = rng.randint(1, 8)
        duration = round(rng.uniform(1, 240), 2)

    return {
        "pu_location_id": rng.randint(1, 243),
        "do_location_id": rng.randint(1, 243),
        "passenger_count": passenger_count,
        "trip_distance": distance,
        "trip_duration_min": duration,
        "pickup_datetime": pickup_time.strftime("%Y-%m-%dT%H:%M:%S"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["normal", "drift"], default="normal")
    parser.add_argument("--count", type=int, default=50, help="Requests to send (1-200).")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--delay-seconds", type=float, default=0.2)
    parser.add_argument(
        "--base-url",
        default=os.environ.get("TAXI_API_BASE_URL", DEFAULT_BASE_URL),
        help="API base URL; defaults to TAXI_API_BASE_URL or the configured AWS API.",
    )
    args = parser.parse_args()
    if not 1 <= args.count <= 200:
        parser.error("--count must be between 1 and 200")
    if args.delay_seconds < 0:
        parser.error("--delay-seconds must be non-negative")

    rng = random.Random(args.seed)
    url = f"{args.base_url.rstrip('/')}/predict/fare"
    for index in range(args.count):
        payload = make_payload(rng, args.mode)
        response = requests.post(url, json=payload, timeout=20)
        response.raise_for_status()
        print(f"{index + 1}/{args.count}: {response.status_code} {response.text}")
        if index + 1 < args.count:
            time.sleep(args.delay_seconds)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
