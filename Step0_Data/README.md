# Step0_Data — baseline cleaning and source-data staging

## What this step does

Step0 is the data-entry point of the repository. It stores the raw input files used across the workflow and runs the first baseline-cleaning notebook. The cleaning notebook standardizes the baseline country-year solid-waste table before WDI feature selection begins.

The step is intentionally separate from the modeling pipeline because later steps repeatedly reuse the source files under `1_Data/`, including SSP drivers and CO2 scenario inputs for future projection.

## Run order

Run the notebook below from the repository root or from `Step0_Data/`:

1. `2_Code/0_clean_baseline.ipynb`

## Main inputs

- `1_Data/` — raw and auxiliary source data used by the workflow.
- Baseline waste-generation source table used by `0_clean_baseline.ipynb`.
- SSP and CO2 driver files later reused by `Step9_FutureProjection`.

## Main outputs

- `3_Results/0_cleaned_baseline.csv` — cleaned baseline panel used by Step1.
- `3_Results/0_cleaning_summary.csv` — cleaning diagnostics and record-level summary.

## Validation focus

- Confirm that the cleaned baseline keeps the expected country-year coverage.
- Confirm that required identifiers such as `Country Code`, `Country Name`, and `Year` remain populated.
- Keep notebook execution output cleared before committing the repository.

## Downstream use

- `Step1_FeaturePool` uses the cleaned baseline to define WDI feature coverage.
- `Step9_FutureProjection` reuses selected raw driver files from `1_Data/`.
