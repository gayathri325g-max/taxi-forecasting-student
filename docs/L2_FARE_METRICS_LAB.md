# L2: Guess the Fare and Feel the Metrics

- **Duration:** 45 to 60 minutes
- **Cloud required:** No
- **Outcome:** A plain-language comparison of fare errors using MAE and RMSE.

## Learning Objectives

1. Distinguish an actual fare from a predicted fare.
2. Calculate signed, absolute, and squared errors.
3. Explain why positive and negative errors can cancel.
4. Interpret MAE and RMSE in dollars.
5. Show why RMSE reacts more strongly to one large miss.

## Part A: Commit Fare Guesses

Complete `Your guess` and `Reason` before viewing Part B.

| Trip | Description | Your guess | Reason |
| --- | --- | ---: | --- |
| A | 1.2 miles, weekday morning, Midtown |  |  |
| B | 2.5 miles, weekday afternoon, Manhattan |  |  |
| C | 4 miles, evening, Manhattan to Brooklyn |  |  |
| D | 8 miles, evening airport route |  |  |
| E | 5.5 miles, late evening, Queens |  |  |

## Part B: Calculate the Shared Errors

Use the convention:

```text
Error = prediction - actual
```

| Trip | Actual fare | Shared prediction | Error | Absolute error | Squared error |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | $10 | $12 |  |  |  |
| B | $15 | $13 |  |  |  |
| C | $20 | $22 |  |  |  |
| D | $30 | $40 |  |  |  |
| E | $25 | $23 |  |  |  |

Complete these calculations:

```text
Sum of signed errors =
Mean signed error =

MAE = sum of absolute errors / 5 =

Mean squared error = sum of squared errors / 5 =
RMSE = square root of mean squared error =
```
Using Error = Actual fare − Shared prediction:

Trip	Actualfare	Sharedprediction  Error 	AbsoluteError	  SquaredError
A	   $10	      $12	            -$2	   $2	              4
B	   $15	      $13	            +$2	   $2	              4
C	   $20	      $22	            -$2	   $2	              4
D	   $30	      $40	            -$10	   $10	           100
E	   $25	      $23	             +$2	   $2	              4

Calculations

Sum of signed errors:  -2 + (+2) + -2 + (+2) + 10 = 10

Mean signed error: 10/5 = 2

MAE: (2+2+2+10+2)/5 = 18/5 = 3.6

Mean squared error: (4+4+4+4+100)/5 = 116/5 = 23.2

RMSE: sqrt(23.2)=4.82
	​


## Part C: Interpret the Baseline

1. What information can the mean signed error hide?
The mean signed error can hide individual prediction errors because positive and negative errors cancel each other out. For example, Trips A, B, C, and E have errors of -2, +2, -2, and +2, which partly cancel. A mean error of -2 therefore does not mean every prediction was only $2 off.
2. What does MAE mean for these five predictions?
The MAE = $3.60 means that, on average, the predictions were $3.60 away from the actual fare, ignoring whether the prediction was too high or too low.
3. Why is RMSE larger than MAE here?
RMSE squares each error before averaging. This gives more weight to large errors. Trip D has a $10 error, which becomes \(10^2 = 100\), substantially increasing RMSE. Therefore, RMSE (4.82) > MAE (3.60).
4. Which trip contributes most to RMSE, and why?
Trip D contributes the most because its error is -$10, much larger than the $2 errors on the other trips. After squaring, its contribution is 100, compared with only 4 for each other trip.
5. Which operational groups should be checked separately before drawing a
   broad conclusion?
You should check groups where prediction behavior might differ, such as:

Short vs. long trips
Peak vs. off-peak hours
Weekdays vs. weekends
Different geographic/route areas
Low-fare vs. high-fare trips
Different vehicle/service types, if applicable

This helps determine whether the overall MAE/RMSE is being driven by a particular operational group rather than representing performance across all trips.
### Verify After Calculating

The recording verifies the hand calculation with the project's metric helpers.
Run this from the repository root after completing the baseline arithmetic:

```powershell
@'
import numpy as np
from src.models.common import mae, rmse

actual = np.array([10, 15, 20, 30, 25], dtype=float)
predicted = np.array([12, 13, 22, 40, 23], dtype=float)
print("MAE:", mae(actual, predicted))
print("RMSE:", rmse(actual, predicted))
'@ | .\.venv\Scripts\python.exe -
```

Compare full precision before rounding to cents. Inspect
[the metric helpers](../src/models/common.py) and
[their tests](../tests/unit/test_models.py). Reversing subtraction changes the
signed error, but not MAE or RMSE after absolute values or squaring.

## Part D: Extreme-Miss Comparison

Change only trip D's prediction from `$40` to `$60`.

| Metric | Baseline | Extreme case | Increase |
| --- | ---: | ---: | ---: |
| MAE |  |  |  |
| RMSE |  |  |  |

Record the changed trip-D values:

```text
Signed error =
Absolute error =
Squared error =
```

After calculating the extreme case, rerun the verification block with only the
fourth prediction changed from `40` to `60`, as in the recording. The actuals
and the other four predictions must stay unchanged.

## Exit Ticket

Complete each statement:

1. Mean signed error can mislead because...
2. MAE means...
3. RMSE is larger in the baseline because...
4. MAE and RMSE should be reported with...

## Completion Check

- All five personal fare guesses are recorded before the shared values appear.
- The shared error table contains signed, absolute, and squared errors.
- MAE and RMSE calculations show the working and retain dollar units.
- Repository code confirms the hand-calculated values.
- The extreme-miss comparison changes only trip D.
- The interpretations state sample size, context, and relevant subgroup checks.