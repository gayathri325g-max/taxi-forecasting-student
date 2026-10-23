"""Publish drift report summaries from S3 to the TaxiForecasting/Drift namespace."""

from __future__ import annotations

import json
import logging
import math
from urllib.parse import unquote_plus

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _metric_data(report: dict) -> list[dict]:
    problem = report.get("problem")
    if not isinstance(problem, str) or not problem:
        raise ValueError("Drift report must contain a non-empty problem.")

    if report.get("status") == "no_data":
        return []

    try:
        drifted_count = float(report["n_drifted"])
        share_drifted = float(report["share_drifted"])
        features = report["features"]
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Drift report is missing valid summary metrics.") from exc

    if not isinstance(features, list):
        raise ValueError("Drift report features must be a list.")
    psi_values = []
    for feature in features:
        if not isinstance(feature, dict) or "psi" not in feature:
            raise ValueError("Each drift feature must contain a PSI value.")
        psi_values.append(float(feature["psi"]))
    max_psi = max(psi_values, default=0.0)

    values = (drifted_count, share_drifted, max_psi)
    if not all(math.isfinite(value) for value in values):
        raise ValueError("Drift summary metrics must be finite numbers.")

    aggregate = [
        {"MetricName": "FeaturesDrifted", "Value": drifted_count, "Unit": "Count"},
        {"MetricName": "ShareDrifted", "Value": share_drifted, "Unit": "None"},
        {"MetricName": "MaxPSI", "Value": max_psi, "Unit": "None"},
    ]
    dimensional = [
        {**metric, "Dimensions": [{"Name": "Problem", "Value": problem}]}
        for metric in aggregate
    ]
    return aggregate + dimensional


def lambda_handler(event: dict, context: object) -> dict:
    """Read an uploaded drift report and publish its summary CloudWatch metrics."""
    try:
        bucket = event["detail"]["bucket"]["name"]
        key = unquote_plus(event["detail"]["object"]["key"])
    except (KeyError, TypeError) as exc:
        raise ValueError("Expected an EventBridge S3 Object Created event.") from exc

    if not key.startswith("drift-reports/") or not key.endswith("drift_metrics.json"):
        logger.info("Ignoring non-report S3 object: s3://%s/%s", bucket, key)
        return {"status": "ignored"}

    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=bucket, Key=key)
    report = json.loads(response["Body"].read())
    if not isinstance(report, dict):
        raise ValueError("Drift report JSON must be an object.")

    metric_data = _metric_data(report)
    if not metric_data:
        logger.info("No captured data in s3://%s/%s; skipping metrics.", bucket, key)
        return {"status": "no_data", "s3_key": key}

    boto3.client("cloudwatch").put_metric_data(
        Namespace="TaxiForecasting/Drift",
        MetricData=metric_data,
    )
    logger.info(
        "Published %d drift metrics from s3://%s/%s",
        len(metric_data),
        bucket,
        key,
    )
    return {"status": "published", "count": len(metric_data), "s3_key": key}
