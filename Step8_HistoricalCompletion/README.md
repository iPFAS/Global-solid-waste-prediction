# Step8_HistoricalCompletion — completed historical panel

## What this step does

Step8 combines observed historical waste records with finalized model predictions to produce a completed country-year panel for 1990 through 2024. For each waste type, the output keeps observed values where available and fills missing historical values with finalized model predictions.

This completed panel is the anchor for future projection and bias correction.

## Run order

1. `1_Code/0_build_historical_completed_panel.ipynb`

## Main inputs

- Finalized predictions from `Step7_ModelTraining/2_Results/1_predictions_all_wastes_long.csv`.
- Wide feature and target data from upstream steps.

## Main outputs

- `2_Results/0_historical_panel_completed.csv`

## Key output fields

- `<waste>_t` — observed raw value when available.
- `<waste>_pred` — finalized model prediction.
- `<waste>_final` — observed value if available, otherwise prediction.
- `<waste>_source` — provenance flag for each final value.

## Validation focus

- Confirm country coverage, year range, and waste-type completeness.
- Confirm that observed values are not overwritten by predictions.
- Confirm that the completed CSV matches the locked paper release output.

## Downstream use

- `Step9_FutureProjection` uses this panel as the 2024 anchor and historical context.
