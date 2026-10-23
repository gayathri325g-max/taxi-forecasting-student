"""Send normal or drift-focused demand requests to the configured Taxi API."""

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
    if mode == "drift":
        # Concentrate current requests on Sunday to shift the captured
        # day_of_week distribution relative to the training data.
        sundays = [
            datetime(2024, 3, day)
            for day in range(1, 32)
            if datetime(2024, 3, day).weekday() == 6
        ]
        target_hour = rng.choice(sundays).replace(hour=rng.randrange(24))
        zone = 132
    else:
        start = datetime(2024, 3, 1)
        end = datetime(2024, 4, 1)
        target_hour = start + timedelta(seconds=rng.randrange(int((end - start).total_seconds())))
        target_hour = target_hour.replace(minute=0, second=0, microsecond=0)
        zone = rng.randint(1, 243)

    return {
        "zone": zone,
        "target_hour": target_hour.strftime("%Y-%m-%dT%H:%M:%S"),
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
    url = f"{args.base_url.rstrip('/')}/predict/demand"
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
