# Model Card — taxi-fare-predictor

_Generated: 2026-10-20 13:53 UTC_

## Model details

- **Problem:** fare
- **Algorithm:** LGBMRegressor
- **Target:** `fare_amount`
- **Registry version:** n/a

## Intended use

Operational forecasting of fare_amount to support fleet positioning and rider fare estimates. Not intended for individual pricing decisions or any use with legal/financial consequences for individuals.

## Evaluation — overall (test split)

| Metric | Value |
|--------|-------|
| rmse | 3.6187 |
| mae | 0.8595 |
| mape | 17.2353 |
| r2 | 0.9582 |

## Evaluation — subgroup fairness

### By borough

Disparity ratio (worst/best RMSE): **5.96** (threshold 1.5) — ⚠️ **flagged**. Worst: `Unknown`, best: `Manhattan`.

| Group | n | RMSE | MAE | MAPE |
|-------|---|------|-----|------|
| Unknown | 1017 | 14.816 | 3.236 | 14.03 |
| Bronx | 502 | 9.456 | 5.874 | 17.15 |
| Queens | 28438 | 8.182 | 2.654 | 21.09 |
| Brooklyn | 2188 | 7.549 | 3.724 | 484.08 |
| Manhattan | 271651 | 2.488 | 0.630 | 12.11 |

### By time_of_day

Disparity ratio (worst/best RMSE): **1.28** (threshold 1.5) — ok. Worst: `overnight`, best: `evening`.

| Group | n | RMSE | MAE | MAPE |
|-------|---|------|-----|------|
| overnight | 32723 | 4.145 | 0.878 | 22.15 |
| morning | 47567 | 4.109 | 1.070 | 29.71 |
| afternoon | 97277 | 3.638 | 0.879 | 13.00 |
| evening | 126233 | 3.240 | 0.760 | 14.52 |

### By day_type

Disparity ratio (worst/best RMSE): **1.05** (threshold 1.5) — ok. Worst: `weekend`, best: `weekday`.

| Group | n | RMSE | MAE | MAPE |
|-------|---|------|-----|------|
| weekend | 170842 | 3.696 | 0.859 | 22.96 |
| weekday | 132958 | 3.517 | 0.860 | 9.88 |

### By holiday

Disparity ratio (worst/best RMSE): **1.00** (threshold 1.5) — ok. Worst: `non-holiday`, best: `non-holiday`.

| Group | n | RMSE | MAE | MAPE |
|-------|---|------|-----|------|
| non-holiday | 303800 | 3.619 | 0.859 | 17.24 |

### By airport

Disparity ratio (worst/best RMSE): **2.54** (threshold 1.5) — ⚠️ **flagged**. Worst: `airport`, best: `non-airport`.

| Group | n | RMSE | MAE | MAPE |
|-------|---|------|-----|------|
| airport | 25337 | 7.625 | 2.283 | 21.33 |
| non-airport | 278463 | 2.999 | 0.730 | 16.86 |

## Top features (SHAP)

| Feature | Mean |SHAP| |
|---------|-----------|
| trip_distance | 6.6533 |
| trip_duration_min | 4.9194 |
| DOLocationID | 0.5276 |
| PULocationID | 0.4278 |
| hour_cos | 0.1210 |
| hour | 0.1130 |
| passenger_count | 0.1076 |
| day_of_week | 0.0442 |
| hour_sin | 0.0310 |
| dow_sin | 0.0267 |

## Limitations

- Trained on a single month of NYC Yellow Taxi data; may not generalise to other periods, boroughs served sparsely, or green/for-hire vehicles.
- Predictions degrade under distribution shift (see drift monitoring).

## Ethical considerations

- No demographic or protected attributes are used or available; fairness is assessed as geographic/temporal service equity, not demographic parity.
- Large borough-level disparities could translate into unequal service quality across neighbourhoods and should be monitored.
