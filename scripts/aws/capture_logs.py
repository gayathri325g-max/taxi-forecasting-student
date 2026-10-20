
import base64
import gzip
import json
import os
import uuid
from datetime import datetime, timezone

import boto3

s3 = boto3.client("s3")
BUCKET = os.environ["CAPTURE_BUCKET"]


def lambda_handler(event, context):
    payload = event["awslogs"]["data"]
    decoded = gzip.decompress(base64.b64decode(payload))
    logs = json.loads(decoded)

    if logs.get("messageType") == "CONTROL_MESSAGE":
        return {"status": "control_message"}

    prediction_events = [
        item for item in logs.get("logEvents", [])
        if item.get("message")
    ]

    if not prediction_events:
        return {"status": "no_events"}

    now = datetime.now(timezone.utc)
    key = (
        f"captured/{now:%Y/%m/%d}/"
        f"{uuid.uuid4().hex}.json"
    )

    body = "\n".join(
        item["message"] for item in prediction_events
    ) + "\n"

    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=body.encode("utf-8"),
        ContentType="application/x-ndjson",
    )

    return {
        "status": "saved",
        "count": len(prediction_events),
        "s3_key": key,
    }
