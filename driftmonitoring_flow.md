# AWS Drift Monitoring and Alerts

This document describes how prediction requests to the Taxi API become drift
alerts. Drift monitoring is a scheduled process: sending requests to the API
does not run the drift check immediately.

## End-to-end flow

1. **The API serves a prediction.** Successful requests to `/predict/demand` and
   `/predict/fare` emit a structured prediction record to the API's
   `taxi.capture` log. The record includes the problem name, captured features,
   prediction, model version, timestamp, and request ID.
2. **CloudWatch Logs forwards prediction records.** A subscription filter selects
   records with `event="prediction"` and invokes the capture Lambda.
3. **The capture Lambda writes to S3.** It stores the log records as newline-
   delimited JSON under the monitoring bucket's `captured/` prefix.
4. **A scheduled SageMaker Processing job checks drift.** When configured, an
   EventBridge Scheduler schedule starts the job at the configured interval.
   The job reads captured records from S3 and compares them with the reference
   training-feature distribution.
5. **The job writes a report to S3.** It writes `drift_metrics.json` to the
   S3 `drift-reports/` prefix. S3 sends an object-created event to EventBridge,
   which invokes the drift-publisher Lambda. The Lambda reads the report from S3
   and publishes `FeaturesDrifted`, `ShareDrifted`, and `MaxPSI` to the
   `TaxiForecasting/Drift` CloudWatch namespace, including per-problem series.
6. **The CloudWatch alarm notifies SNS.** The feature-drift alarm enters `ALARM`
   when `FeaturesDrifted` is at least `1` in its 24-hour evaluation period.
   Its alarm action publishes to the configured SNS topic.
7. **SNS delivers the notification.** If an email subscription is configured,
   SNS emails that address after the recipient confirms the subscription.

## What the drift job measures

The job calculates PSI and KS statistics for comparable numeric features. In
this implementation, a feature is marked as drifted when its PSI is at least
`0.2`; the KS statistic and p-value are supporting context. The aggregate
`FeaturesDrifted` metric is the number of features flagged in that run.

Drift is a signal to investigate. It is not proof that model performance has
degraded and does not automatically start retraining or deploy a new model.

## Configuration and prerequisites

The AWS resources in `infra/terraform/monitoring.tf` are gated by
`enable_monitoring`. For the end-to-end flow to work:

- Monitoring must be enabled and its Terraform changes applied.
- The API CloudWatch log group, subscription filter, capture Lambda, and
  monitoring S3 bucket must be provisioned and operating.
- A monitoring image URI must be configured to create the scheduled
  SageMaker drift Processing job. The S3 bucket must send events to EventBridge
  so each uploaded drift report invokes the publisher Lambda.
- An SNS email subscription requires a non-empty `alert_email`, and the
  recipient must confirm the subscription.
- The SageMaker execution role must be able to read captured inputs and write
  drift reports. The publisher Lambda role must be able to read reports and
  publish CloudWatch metrics.
- Captured requests must exist in the S3 prefix read by the drift job.

The drift schedule currently runs one problem per job. The Terraform variable
`drift_problem` defaults to `fare`; set it to `demand` to check demand instead.
To monitor both, configure separate runs or schedules for each problem.

## Limitations for demand monitoring

The demand API currently captures `zone`, `hour_of_day`, and `day_of_week`.
Demand model features such as lagged pickup counts and rolling-window
statistics are not included in the capture record, so this monitoring flow
cannot check drift in those inputs from API logs.

## Sending test requests

The `demand_post_reqs.py` and `fare_post_reqs.py` scripts can send normal or
drift-focused example requests to the configured API. Those requests only
populate the capture path if the AWS logging and Lambda-to-S3 components above
are configured. The drift report is produced later, when the scheduled SageMaker Processing job
runs (or when that job is started manually); uploading the report triggers
CloudWatch metric publication.
Synthetic drift traffic is for testing and is not representative of genuine
production traffic.

## Related implementation

- API prediction logging: `src/serving/api.py`
- Capture Lambda: `infra/terraform/capture_logs.py`
- Drift metric publisher Lambda: `infra/terraform/publish_drift_metrics.py`
- AWS resources, alarms, SNS, and schedules: `infra/terraform/monitoring.tf`
- Drift job: `scripts/monitoring/run_drift_job.py`
- Drift calculation: `src/monitoring/drift.py`
- Request generators: `demand_post_reqs.py` and `fare_post_reqs.py`
