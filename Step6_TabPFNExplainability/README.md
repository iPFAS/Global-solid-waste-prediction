# Step6_TabPFNExplainability — TabPFN interpretation and mechanism checks

## What this step does

Step6 explains and stress-tests the selected TabPFN strategy. It computes full-feature Borda-style importance, runs core-feature ablations, and compares pooled versus per-waste bridge behavior.

The step supports the modeling choice with feature-level and mechanism-level diagnostics before final model training.

## Run order

1. `1_Code/0_tabpfn_winner_full_feature_borda_importance.ipynb`
2. `1_Code/1_tabpfn_core_feature_ablation.ipynb`
3. `1_Code/2_tabpfn_pooled_vs_per_waste_bridge.ipynb`

## Main inputs

- Step5 rankings and prediction outputs from `Step5_ModelComparison/2_Results/`.
- Feature contracts and processed model inputs from `Step4_ModelInputs/2_Results/`.

## Main outputs

- Feature importance summaries under `2_Results/`.
- Core-feature ablation results under `2_Results/`.
- Pooled-versus-per-waste bridge diagnostics under `2_Results/`.

## Validation focus

- Confirm that importance calculations use the winning model family output.
- Confirm that ablation comparisons use the same folds and metrics as Step5.
- Confirm that bridge diagnostics are consistent with the final training strategy.

## Downstream use

- `Step7_ModelTraining` uses the selected feature and modeling decisions from this step.
