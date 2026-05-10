# Step9_FutureProjection — SSP projections and uncertainty bands

## What this step does

Step9 projects solid-waste generation from the historical anchor into SSP scenarios through 2100. It builds SSP future drivers, transforms future feature matrices with the final Step7 preprocessing contracts, predicts waste generation, applies 2024 anchor bias correction, estimates uncertainty from temporal backtests, and exports global uncertainty bands.

The current repository intentionally keeps the lean prediction schema. Legacy PI90/P90 columns from earlier uncertainty experiments are not retained.

## Run order

1. `1_Code/0_build_future_features.ipynb` — builds SSP population, GDP, density, and CO2 driver panels; exports raw and transformed future feature matrices.
2. `1_Code/1_predict_future_and_assemble_panel.ipynb` — loads final Step7 models, predicts future waste generation, and assembles the historical-plus-future super panel.
3. `1_Code/2_apply_anchor_bias_correction.ipynb` — applies 2024 anchor bias factors and trend bridging to corrected future values.
4. `1_Code/3_temporal_backtest_uncertainty.ipynb` — performs temporal holdout backtesting and estimates error as a function of forecast horizon.
5. `1_Code/4_apply_uncertainty_bands.ipynb` — applies the backtest-derived uncertainty curve to SSP global totals.

## Main inputs

- SSP driver file from `Step0_Data/1_Data/SSP/`.
- CO2 scenario file from `Step0_Data/1_Data/CO2/`.
- Final feature contracts, preprocessing pipelines, and model artifacts from `Step7_ModelTraining/2_Results/`.
- Completed historical panel from `Step8_HistoricalCompletion/2_Results/0_historical_panel_completed.csv`.

## Main outputs

- `2_Results/0_future_driver_panel.csv`
- `2_Results/0_future_feature_matrix_raw.csv`
- `2_Results/0_future_features_transformed_<waste>.csv`
- `2_Results/1_ssp_predictions_long.csv`
- `2_Results/1_super_panel_1990_2100.csv`
- `2_Results/2_anchor_bias_factors.csv`
- `2_Results/2_super_panel_1990_2100.csv`
- `2_Results/3_temporal_backtest_results.csv`
- `2_Results/3_global_error_vs_horizon.csv`
- `2_Results/4_ssp_with_uncertainty_bands.csv`
- `2_Results/4_ssp_global_total_summary.csv`

## Validation focus

- Confirm that future country coverage includes the expected 173 SSP-mapped countries.
- Confirm that the 0_, 2_, 3_, and 4_ CSV outputs match the locked paper release outputs where applicable.
- Confirm that the common columns of the 1_ super-panel outputs match the release values exactly while excluding legacy PI90/P90 fields.
- Keep all notebooks output-free before committing.
