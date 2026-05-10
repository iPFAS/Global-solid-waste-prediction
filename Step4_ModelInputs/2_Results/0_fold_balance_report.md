# NBCP-CV Fold Balance Report

This report summarizes outer 5-fold balance under NBCP-CV.

## Fold Summary

|   outer_fold |   n_rows |   n_countries |   n_years |     wg_mean |   wg_median |   log_wg_mean |
|-------------:|---------:|--------------:|----------:|------------:|------------:|--------------:|
|            1 |     4011 |            36 |        35 | 6.14844e+07 | 4.15893e+06 |       14.8988 |
|            2 |     4011 |            37 |        35 | 3.27332e+07 | 4.59856e+06 |       14.9678 |
|            3 |     4011 |            35 |        35 | 3.18405e+07 | 5.586e+06   |       15.0097 |
|            4 |     4011 |            37 |        35 | 1.37198e+07 | 3.48867e+06 |       14.5695 |
|            5 |     4011 |            37 |        35 | 1.7542e+07  | 4.68171e+06 |       14.9946 |

## IncomeGroup by Fold (Country Count)

|   outer_fold |   High income |   Low income |   Lower middle income |   Upper middle income |
|-------------:|--------------:|-------------:|----------------------:|----------------------:|
|            1 |            13 |            4 |                     9 |                    10 |
|            2 |            13 |            4 |                    10 |                    10 |
|            3 |            12 |            4 |                     9 |                    10 |
|            4 |            13 |            4 |                    10 |                    10 |
|            5 |            13 |            4 |                    10 |                    10 |

## Gap Diagnostics

- row_gap: 0
- row_gap_rel: 0.000000

### IncomeGroup Spread (max-min)

| IncomeGroup         |   spread |
|:--------------------|---------:|
| High income         |        1 |
| Lower middle income |        1 |
| Low income          |        0 |
| Upper middle income |        0 |
