# Step1_FeaturePool — WDI coverage scan and feature-panel assembly

## What this step does

Step1 determines which World Development Indicators are usable for global solid-waste prediction. The first notebook scans candidate WDI variables for country-year coverage. The second notebook builds the selected feature panel that is carried into imputation.

This step fixes the feature pool before missing-value treatment, so it controls the economic, demographic, urbanization, sectoral, and emissions predictors available to the modeling workflow.

## Run order

1. `1_Code/0_scan_wdi_coverage.ipynb` — scans WDI coverage and identifies usable candidate variables.
2. `1_Code/1_build_selected_feature_panel.ipynb` — constructs the selected country-year feature panel.

## Main inputs

- `Step0_Data/3_Results/0_cleaned_baseline.csv`
- Raw WDI files staged under `Step0_Data/1_Data/`

## Main outputs

- WDI coverage diagnostics under `2_Results/`.
- Selected feature panel under `2_Results/`, used by Step2.

## Validation focus

- Check that selected indicators have sufficient country-year coverage.
- Check that the selected feature panel preserves the baseline country-year keys.
- Keep the selected feature list stable before running Step2 and later modeling steps.

## Downstream use

- `Step2_WDI_Features` imputes the selected panel.
- Later modeling steps rely on the feature pool fixed here.
