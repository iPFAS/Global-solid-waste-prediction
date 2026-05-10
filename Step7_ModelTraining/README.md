# Step7_ModelTraining — final training assets and finalized models

## What this step does

Step7 prepares the final training assets and trains the finalized models used for historical completion and future projection. It exports raw and processed training contracts, final preprocessing pipelines, per-waste model artifacts, prediction tables, and mixed-versus-waste-specific comparison outputs.

This step is the bridge between model selection and production-style prediction files.

## Run order

1. `1_Code/0_prepare_training_assets.ipynb` — builds final raw and processed training assets.
2. `1_Code/1_train_finalize_models.ipynb` — trains and exports finalized per-waste models.
3. `1_Code/2_train_mixed_finalize_comparison.ipynb` — compares mixed and waste-specific finalization behavior.

## Main inputs

- Selected feature contracts and model-family decisions from Steps 4 through 6.
- Long modeling table and final training labels from upstream data steps.

## Main outputs

- `2_Results/0_training_raw_<waste>.csv`
- `2_Results/0_training_processed_<waste>.csv`
- `2_Results/0_feature_contract_raw.csv`
- `2_Results/0_feature_contract_processed.csv`
- `2_Results/1_finalize_model_<waste>.pkl`
- Final prediction, ranking, and mechanism comparison tables.

## Validation focus

- Confirm that raw and processed feature contracts match the exported pipelines.
- Confirm that model artifacts exist for all four waste types.
- Confirm that prediction files are complete for downstream Step8 and Step9.

## Reproducibility notes

- Some finalized model artifacts are locked to the paper release version because model training can vary by environment.
