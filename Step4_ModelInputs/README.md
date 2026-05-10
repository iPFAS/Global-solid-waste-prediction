# Step4_ModelInputs — outer-CV folds and comparison views

## What this step does

Step4 turns the long table into reproducible model inputs. It creates the outer cross-validation base, assigns folds, builds processed train/test inputs, and exports comparison views used by model-family evaluation.

This step defines the evaluation frame for Step5, so fold balance and feature-contract stability are the main concerns.

## Run order

1. `1_Code/0_build_outercv_base.ipynb` — builds the outer-CV base table and fold definitions.
2. `1_Code/1_build_comparison_views.ipynb` — exports processed comparison views for model families.

## Main inputs

- `Step3_BuildLongTable/2_Results/0_LongTable_SetABC.csv`

## Main outputs

- Fold-specific train/test inputs under `2_Results/`.
- Feature-column contracts under `2_Results/`.
- `2_Results/0_fold_balance_report.md` for fold coverage diagnostics.

## Validation focus

- Confirm that outer folds preserve temporal ordering and country-year integrity.
- Confirm that train/test files contain the same feature contract where required.
- Confirm that target leakage columns are excluded from feature matrices.

## Downstream use

- `Step5_ModelComparison` consumes the processed folds and feature contracts.
