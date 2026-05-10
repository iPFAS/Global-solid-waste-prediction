# Step2_WDI_Features — WDI feature imputation

## What this step does

Step2 fills missing values in the selected WDI feature panel. It produces a complete country-year feature table that can be merged with waste-generation targets and reshaped into the long modeling format.

The step is responsible for keeping feature values numerically usable while preserving country, year, income-group, region, and waste-target columns needed downstream.

## Run order

1. `1_Code/0_impute_wdi_features.ipynb`

## Main inputs

- Selected feature panel from `Step1_FeaturePool/2_Results/`.
- Cleaned baseline identifiers and target columns from `Step0_Data/3_Results/`.

## Main outputs

- `2_Results/1_imputed_features_data.csv` — imputed wide table consumed by Step3.
- Imputation diagnostics under `2_Results/`.

## Validation focus

- Confirm that required WDI feature columns have no unexpected missing values after imputation.
- Confirm that waste target columns are not altered by feature imputation.
- Confirm that country-year keys remain unique.

## Downstream use

- `Step3_BuildLongTable` reshapes the imputed wide table into one row per waste type.
