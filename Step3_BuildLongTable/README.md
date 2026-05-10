# Step3_BuildLongTable — wide-to-long modeling table

## What this step does

Step3 converts the imputed wide country-year table into a long supervised-learning table. Each available waste target is turned into a separate row with a `Waste_Generation_t` label and waste-type indicators.

The notebook also creates log proxy features and waste-type interaction proxies used by the downstream model-input construction.

## Run order

1. `1_Code/0_build_long_table.ipynb`

## Main inputs

- `Step2_WDI_Features/2_Results/1_imputed_features_data.csv`

## Main outputs

- `2_Results/0_LongTable_SetABC.csv` — long table used by Step4.

## Key transformations

- Converts `AW_t`, `CDW_t`, `IW_t`, and `MSW_t` from wide target columns into long waste-type rows.
- Creates `Waste_Generation_t` as the raw target value.
- Adds waste-type indicator columns and proxy interaction columns.

## Validation focus

- Confirm that every long row has exactly one active waste type.
- Confirm that row counts match the number of non-missing waste target observations.
- Confirm that proxy features are finite where base features are valid.
