# Model Card — taxi-demand-forecaster

_Generated: 2026-10-20 13:53 UTC_

## Model details

- **Problem:** demand
- **Algorithm:** CatBoostRegressor
- **Target:** `pickup_count`
- **Registry version:** n/a

## Intended use

Operational forecasting of pickup_count to support fleet positioning and rider fare estimates. Not intended for individual pricing decisions or any use with legal/financial consequences for individuals.

## Evaluation — overall (test split)

| Metric | Value |
|--------|-------|
| rmse | 8.5353 |
| mae | 2.6657 |
| mape | 42.0733 |
| r2 | 0.9648 |

## Evaluation — subgroup fairness

### By borough

Disparity ratio (worst/best RMSE): **185.24** (threshold 1.5) — ⚠️ **flagged**. Worst: `Manhattan`, best: `EWR`.

| Group | n | RMSE | MAE | MAPE |
|-------|---|------|-----|------|
| Manhattan | 3801 | 14.931 | 8.168 | 29.14 |
| Queens | 3971 | 7.275 | 1.331 | 58.88 |
| Unknown | 116 | 3.316 | 2.210 | 45.37 |
| Brooklyn | 3514 | 0.833 | 0.471 | 59.89 |
| Bronx | 2481 | 0.380 | 0.227 | 74.96 |
| Staten Island | 632 | 0.097 | 0.060 | 95.32 |
| EWR | 58 | 0.081 | 0.060 | nan |

### By time_of_day

Disparity ratio (worst/best RMSE): **2.04** (threshold 1.5) — ⚠️ **flagged**. Worst: `evening`, best: `morning`.

| Group | n | RMSE | MAE | MAPE |
|-------|---|------|-----|------|
| evening | 4554 | 11.016 | 3.447 | 40.17 |
| afternoon | 3947 | 8.490 | 3.030 | 38.11 |
| overnight | 3036 | 6.703 | 1.832 | 50.98 |
| morning | 3036 | 5.389 | 1.854 | 43.23 |

### By day_type

Disparity ratio (worst/best RMSE): **1.19** (threshold 1.5) — ok. Worst: `weekday`, best: `weekend`.

| Group | n | RMSE | MAE | MAPE |
|-------|---|------|-----|------|
| weekday | 2429 | 9.820 | 3.315 | 35.84 |
| weekend | 12144 | 8.254 | 2.536 | 43.41 |

### By holiday

Disparity ratio (worst/best RMSE): **1.00** (threshold 1.5) — ok. Worst: `non-holiday`, best: `non-holiday`.

| Group | n | RMSE | MAE | MAPE |
|-------|---|------|-----|------|
| non-holiday | 14573 | 8.535 | 2.666 | 42.07 |

### By airport

Disparity ratio (worst/best RMSE): **5.48** (threshold 1.5) — ⚠️ **flagged**. Worst: `airport`, best: `non-airport`.

| Group | n | RMSE | MAE | MAPE |
|-------|---|------|-----|------|
| airport | 115 | 42.220 | 30.434 | 48.80 |
| non-airport | 14458 | 7.698 | 2.445 | 41.94 |

## Top features (SHAP)

| Feature | Mean |SHAP| |
|---------|-----------|
| lag_168 | 8.4608 |
| lag_1 | 6.6017 |
| lag_24 | 4.7778 |
| lag_2 | 2.3604 |
| rolling_mean_24 | 2.0456 |
| lag_3 | 1.0048 |
| rolling_mean_3 | 0.8368 |
| hour_cos | 0.7824 |
| hour | 0.5016 |
| rolling_mean_168 | 0.4914 |

## Limitations

- Trained on a single month of NYC Yellow Taxi data; may not generalise to other periods, boroughs served sparsely, or green/for-hire vehicles.
- Predictions degrade under distribution shift (see drift monitoring).

## Ethical considerations

- No demographic or protected attributes are used or available; fairness is assessed as geographic/temporal service equity, not demographic parity.
- Large borough-level disparities could translate into unequal service quality across neighbourhoods and should be monitored.
